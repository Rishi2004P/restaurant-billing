import streamlit as st
import sqlite3
import datetime
import pandas as pd
import io
from fpdf import FPDF
import os
import sys
import traceback
import time
import qrcode
from PIL import Image
import re
import xlsxwriter
import hashlib

# --- User Management (For demonstration only - use a secure method in production) ---
USERS = {
    "admin": "password123", # Replace with actual hashed passwords
    "cashier": "cashierpass",
    # You can add more users
}

def check_credentials(username, password):
    """Checks if the provided username and password are valid."""
    # In a real app, hash the input password and compare with hashed stored password
    return USERS.get(username) == password

# --- Import custom modules ---
# Allow importing from project root for the database connection and PDF generator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    # Assuming pdf_generator.py is in a 'utils' directory relative to the script
    from utils.pdf_generator import generate_pdf_bill
except ImportError:
    st.error("Error: `utils.pdf_generator` module not found. PDF generation will not work. Please ensure `pdf_generator.py` is in the `utils` folder.")
    def generate_pdf_bill(*args, **kwargs):
        st.warning("PDF generation function is not available.")
        return b"PDF generation not available."

# --- Try to import Plotly, with a fallback if it's not installed ---
try:
    import plotly.express as px
    plotly_available = True
except ImportError:
    plotly_available = False
    st.warning("Plotly not found. Using basic Streamlit charts instead. For interactive charts, please install plotly with 'pip install plotly'.")

# --- Initial Setup ---
st.set_page_config(page_title="🍽️ Restaurant Billing System", layout="wide")

# Initialize session state variables if they don't exist
if 'success_message' not in st.session_state:
    st.session_state['success_message'] = None
if 'selected_quantities' not in st.session_state:
    st.session_state['selected_quantities'] = {}
if 'payment_method_selected' not in st.session_state:
    st.session_state['payment_method_selected'] = None
if 'is_order_submitted' not in st.session_state:
    st.session_state['is_order_submitted'] = False
if 'confirm_clear' not in st.session_state:
    st.session_state['confirm_clear'] = False
if 'edit_item_id' not in st.session_state:
    st.session_state['edit_item_id'] = None
if 'active_page' not in st.session_state:
    st.session_state['active_page'] = "Place Order"
if 'debug_menu' not in st.session_state:
    st.session_state.debug_menu = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""


# ----------------- DB Helpers -----------------
def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'restaurant.db')
    return sqlite3.connect(db_path)

def setup_database():
    """
    Sets up the initial database and tables if they don't exist.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            gst REAL NOT NULL,
            image_url TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            mode TEXT NOT NULL,
            payment TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            total REAL NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER,
            order_id INTEGER,
            qty INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (item_id) REFERENCES menu (item_id),
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        );
    """)
    conn.commit()
    conn.close()

def sanitize_menu_image_urls():
    """
    Finds and replaces any invalid image URLs in the database with a placeholder.
    """
    conn = get_connection()
    cur = conn.cursor()
    placeholder_image = "https://placehold.co/100x100/600/fff?text=No+Image"
    
    try:
        cur.execute("SELECT item_id, image_url FROM menu")
        items = cur.fetchall()
        count = 0
        for item_id, image_url in items:
            if not isinstance(image_url, str):
                cur.execute(
                    "UPDATE menu SET image_url = ? WHERE item_id = ?",
                    (placeholder_image, item_id)
                )
                count += 1
                continue
            
            is_valid_url = image_url.strip().startswith(('http', 'data:image'))
            
            if not is_valid_url:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                full_path = os.path.join(base_dir, '..', image_url)
                
                if not os.path.exists(full_path):
                    st.warning(f"Invalid local image path found for item {item_id}: {image_url}. Replacing with placeholder.")
                    cur.execute(
                        "UPDATE menu SET image_url = ? WHERE item_id = ?",
                        (placeholder_image, item_id)
                    )
                    count += 1
            
        conn.commit()
        if count > 0:
            st.info(f"Automatically sanitized {count} invalid image URLs in the database on startup.")
    except Exception as e:
        st.error(f"Error sanitizing database: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_menu_items():
    """
    Reads menu items from the database and sanitizes image URLs on the fly.
    """
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM menu", conn)
    conn.close()
    return df

def get_menu_dict():
    """
    Creates a dictionary of menu items for quick lookup.
    """
    df = get_menu_items()
    if not df.empty:
        return df.set_index('item_id').to_dict('index')
    return {}

@st.cache_data(ttl=60)
def get_orders(start_date=None, end_date=None, order_id=None):
    conn = get_connection()
    query = "SELECT * FROM orders"
    params = []
    where_clauses = []
    if order_id:
        where_clauses.append("order_id = ?")
        params.append(order_id)
    if start_date:
        where_clauses.append("timestamp BETWEEN ? AND ?")
        params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        params.append(end_date.strftime("%Y-%m-%d 23:59:59"))
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_order_items(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_id, qty, total FROM order_items WHERE order_id = ?", (order_id,))
    items = cur.fetchall()
    conn.close()
    return items

def save_order_to_db(order_data: dict) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO orders (mode, payment, timestamp, total)
            VALUES (?, ?, ?, ?)
            """,
            (str(order_data['mode']), str(order_data['payment']),
             str(order_data['timestamp']), float(order_data['total']))
        )
        order_id = cur.lastrowid
        for item in order_data['items']:
            cur.execute(
                """
                INSERT INTO order_items (item_id, order_id, qty, total)
                VALUES (?, ?, ?, ?)
                """,
                (int(item['item_id']), int(order_id),
                 int(item['qty']), float(item['total']))
            )
        conn.commit()
        st.cache_data.clear()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def clear_orders_db():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM order_items")
        cur.execute("DELETE FROM orders")
        conn.commit()
        st.success("All orders cleared successfully!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error clearing orders: {e}")
        st.code(traceback.format_exc())
    finally:
        conn.close()

def add_menu_item_to_db(item_name, category, price, gst, image_url):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO menu (item_name, category, price, gst, image_url) VALUES (?, ?, ?, ?, ?)",
            (item_name, category, price, gst, image_url)
        )
        conn.commit()
        st.success(f"Item '{item_name}' added successfully!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error adding menu item: {e}")
    finally:
        conn.close()

def update_menu_item_in_db(item_id, item_name, category, price, gst, image_url):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE menu
            SET item_name = ?, category = ?, price = ?, gst = ?, image_url = ?
            WHERE item_id = ?
            """,
            (item_name, category, price, gst, image_url, item_id)
        )
        conn.commit()
        st.success(f"Item '{item_name}' updated successfully!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error updating menu item: {e}")
    finally:
        conn.close()

def delete_menu_item_from_db(item_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM menu WHERE item_id = ?", (item_id,))
        conn.commit()
        st.success("Item deleted successfully!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error deleting menu item: {e}")
    finally:
        conn.close()

# --- Analytics Functions using DataFrames ---
def get_sales_by_date(start_date, end_date):
    conn = get_connection()
    query = """
    SELECT
        DATE(timestamp) AS order_date,
        SUM(total) AS daily_sales
    FROM
        orders
    WHERE
        timestamp BETWEEN ? AND ?
    GROUP BY
        order_date
    ORDER BY
        order_date
    """
    params = [start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d 23:59:59")]
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_sales_by_payment_method(start_date, end_date):
    conn = get_connection()
    query = """
    SELECT
        payment,
        SUM(total) AS total_sales
    FROM
        orders
    WHERE
        timestamp BETWEEN ? AND ?
    GROUP BY
        payment
    """
    params = [start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d 23:59:59")]
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_total_revenue(start_date, end_date):
    conn = get_connection()
    query = "SELECT SUM(total) FROM orders WHERE timestamp BETWEEN ? AND ?"
    params = [start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d 23:59:59")]
    total_revenue = pd.read_sql(query, conn, params=params).iloc[0, 0]
    conn.close()
    return total_revenue if total_revenue is not None else 0

def get_num_orders(start_date, end_date):
    conn = get_connection()
    query = "SELECT COUNT(*) FROM orders WHERE timestamp BETWEEN ? AND ?"
    params = [start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d 23:59:59")]
    num_orders = pd.read_sql(query, conn, params=params).iloc[0, 0]
    conn.close()
    return num_orders

def get_sales_by_category(start_date, end_date):
    conn = get_connection()
    menu_items_df = get_menu_items()
    
    query = """
    SELECT
        oi.item_id,
        oi.qty
    FROM
        order_items oi
    JOIN
        orders o ON oi.order_id = o.order_id
    WHERE
        o.timestamp BETWEEN ? AND ?
    """
    params = [start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")]
    order_items_df = pd.read_sql(query, conn, params=params)
    conn.close()
    
    if order_items_df.empty:
        return pd.DataFrame(columns=['category', 'total_sales'])
        
    merged_df = pd.merge(order_items_df, menu_items_df, on='item_id')
    merged_df['total_sales'] = merged_df['qty'] * merged_df['price']
    
    category_sales = merged_df.groupby('category')['total_sales'].sum().reset_index()
    return category_sales

@st.cache_data
def get_most_sold_items(start_date=None, end_date=None, top_n=5):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT
        oi.item_id,
        SUM(oi.qty) as total_qty_sold
    FROM
        order_items oi
    JOIN
        orders o ON oi.order_id = o.order_id
    """
    params = []
    if start_date and end_date:
        query += " WHERE o.timestamp BETWEEN ? AND ?"
        params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        params.append(end_date.strftime("%Y-%m-%d 23:59:59"))
    query += """
    GROUP BY
        oi.item_id
    ORDER BY
        total_qty_sold DESC
    LIMIT ?
    """
    params.append(top_n)
    cur.execute(query, tuple(params))
    most_sold = cur.fetchall()
    conn.close()
    
    menu_df = get_menu_items()
    menu_dict = menu_df.set_index('item_id')['item_name'].to_dict() if not menu_df.empty else {}
    
    return [(menu_dict.get(item_id, f"Item {item_id}"), qty) for item_id, qty in most_sold]

# --- UPI QR Code Generation Function ---
def generate_upi_qr_code(amount):
    """
    Generates a UPI payment QR code as a PIL Image.
    """
    upi_id = "your_upi_id@bank"
    business_name = "Imperial Spice"
    
    txn_id = f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    upi_link = f"upi://pay?pa={upi_id}&pn={business_name}&am={amount:.2f}&tid={txn_id}&cu=INR"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def pil_to_bytes(img):
    """
    Converts a PIL Image object to a byte stream.
    """
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ----------------- CSV & PDF Download -----------------
def generate_csv(order_id: int) -> str:
    conn = get_connection()
    query = """
    SELECT m.item_name, oi.qty, oi.total
    FROM order_items oi
    JOIN menu m ON oi.item_id = m.item_id
    WHERE oi.order_id = ?
    """
    df = pd.read_sql(query, conn, params=(order_id,))
    conn.close()
    return df.to_csv(index=False)

# --- Ensure DB setup runs on first load ---
setup_database()
sanitize_menu_image_urls()


# ----------------- UI -----------------

# --- NEW STYLISH LOGIN PAGE ---
if not st.session_state['logged_in']:
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #1f283d, #2d3b53);
                color: white;
            }
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .login-card {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                width: 100%;
                max-width: 400px;
            }
            .main-header {
                font-size: 2.5em;
                font-weight: bold;
                text-align: center;
                margin-bottom: 0.5em;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .subheader {
                font-size: 1.2em;
                text-align: center;
                color: #e0e0e0;
                margin-bottom: 2em;
            }
            .stTextInput>div>div>input {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                color: white;
                padding: 10px;
            }
            .stTextInput>div>div>input::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            .stButton>button {
                width: 100%;
                background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 1.1em;
                cursor: pointer;
                box-shadow: 0 4px 15px 0 rgba(100, 100, 200, 0.5);
                transition: transform 0.2s;
            }
            .stButton>button:hover {
                transform: scale(1.02);
            }
            .stAlert {
                border-radius: 12px;
            }
            /* Hide the sidebar in the login page */
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        <div class="login-container">
            <div class="login-card">
                <h1 class="main-header">🍽️ Imperial Spice</h1>
                <h3 class="subheader">Restaurant Billing System</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # We use columns to center the login form itself within the card
    col_empty_left, col_form, col_empty_right = st.columns([1, 2, 1])

    with col_form:
        # Use a form inside the custom-styled card
        with st.form("login_form", clear_on_submit=False):
            st.markdown("#### Login", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            message_placeholder = st.empty()

            login_button = st.form_submit_button("Login")

            if login_button:
                if check_credentials(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    message_placeholder.success(f"Welcome, **{username}**! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    message_placeholder.error("❌ Invalid username or password. Please try again.")
                    st.session_state['logged_in'] = False
                    st.session_state['username'] = ""

# --- Main application UI ---
else:
    # Sidebar is visible now
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['active_page'] = "Place Order"
        st.success("You have been logged out.")
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Place Order", "Menu Management", "Order History", "Analytics Dashboard"], key='navigation_radio')

    st.sidebar.markdown("---")
    st.sidebar.subheader("Database Debugging")
    if st.sidebar.button("Show Raw Menu Data"):
        conn = get_connection()
        raw_menu_df = pd.read_sql("SELECT * FROM menu", conn)
        conn.close()
        st.session_state.debug_menu = raw_menu_df
    if st.session_state.debug_menu is not None:
        st.sidebar.dataframe(st.session_state.debug_menu)
    
    # ----------------- Place Order Page -----------------
    if page == "Place Order":
        st.title("🍽️ Place a New Order")
        
        success_placeholder = st.empty()
        
        if st.session_state['success_message']:
            with success_placeholder.container():
                st.success(st.session_state['success_message'])
                order_id = st.session_state['last_order_id']
                st.download_button(
                    label="📥 Download Receipt (CSV)",
                    data=generate_csv(order_id),
                    file_name=f"receipt_order_{order_id}.csv",
                    mime="text/csv"
                )
                
                orders_df = get_orders(order_id=order_id)
                if not orders_df.empty:
                    order_details = orders_df.iloc[0]
                    items_raw = get_order_items(order_id)
                    menu_dict = get_menu_dict()

                    order_items_for_pdf = []
                    subtotal_before_gst = 0
                    gst_amount = 0
                    for item_id, qty, item_total_with_gst in items_raw:
                        item_details = menu_dict.get(item_id, {})
                        unit_price = item_details.get("price", 0)
                        item_name = item_details.get("item_name", f"Item {item_id}")
                        
                        base_total_for_item = unit_price * qty
                        gst_for_item = item_total_with_gst - base_total_for_item
                        
                        subtotal_before_gst += base_total_for_item
                        gst_amount += gst_for_item

                        order_items_for_pdf.append({
                            "item": item_name,
                            "qty": qty,
                            "price": unit_price,
                            "total": item_total_with_gst
                        })

                    final_total_from_db = float(order_details['total'])
                    discount_for_pdf = 0
                    
                    try:
                        pdf_bytes = generate_pdf_bill(
                            order_id=order_id,
                            order_items=order_items_for_pdf,
                            subtotal=subtotal_before_gst, 
                            gst=gst_amount,
                            discount=discount_for_pdf,
                            total=final_total_from_db,
                            payment_method=order_details['payment'],
                            mode=order_details['mode']
                        )
                        
                        st.download_button(
                            label="📥 Download Receipt (PDF)",
                            data=pdf_bytes,
                            file_name=f"receipt_order_{order_id}.pdf",
                            mime="application/pdf"
                        )
                    except NameError:
                        st.warning("`generate_pdf_bill` not found. PDF generation will not work.")
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
                        st.code(traceback.format_exc())

                if st.button("Start New Order"):
                    st.session_state['success_message'] = None
                    st.session_state['selected_quantities'] = {}
                    st.session_state['payment_method_selected'] = None
                    st.session_state['is_order_submitted'] = False
                    st.session_state.pop('last_order_id', None)
                    st.cache_data.clear()
                    st.rerun()
        else:
            order_mode = st.radio("Select Order Mode:", ["Dine-In", "Takeaway"], key='order_mode_radio')
            st.write(f"📝 Current Mode: **{order_mode}**")
        
            menu_items_df = get_menu_items()
        
            st.subheader("📋 Select Items")
            all_categories = sorted(list(set(menu_items_df['category'])))
            selected_category = st.selectbox("Select a Category:", all_categories, index=0, key='category_select')
            display_items = menu_items_df[menu_items_df['category'] == selected_category]
            
            base_dir = os.path.dirname(os.path.abspath(__file__))

            for index, row in display_items.iterrows():
                item_id = row['item_id']
                if item_id not in st.session_state['selected_quantities']:
                    st.session_state['selected_quantities'][item_id] = 0
                
                col_img, col_info, col_qty = st.columns([1, 3, 2])
                
                image_url = row['image_url']
                if isinstance(image_url, str) and image_url.strip().startswith(('http', 'data:image')):
                    image_to_display = image_url
                else:
                    local_path_candidate = os.path.join(base_dir, '..', image_url if isinstance(image_url, str) else "")
                    if os.path.exists(local_path_candidate):
                        image_to_display = local_path_candidate
                    else:
                        image_to_display = "https://placehold.co/100x100/600/fff?text=No+Image"
                
                with col_img:
                    st.image(image_to_display, width=80, caption=row['item_name'])
                with col_info:
                    st.markdown(f"**{row['item_name']}** - ₹{row['price']}")
                with col_qty:
                    qty = st.number_input(f"Qty for {row['item_name']}", min_value=0, max_value=20, step=1, key=f"qty_{item_id}", value=st.session_state['selected_quantities'][item_id])
                    st.session_state['selected_quantities'][item_id] = qty
                
                if qty > 0:
                    base_total = float(row['price']) * int(qty)
                    gst_amount = base_total * float(row['gst']) / 100.0
                    item_total = base_total + gst_amount
                    st.markdown(f"**Price:** ₹{base_total:.2f} + **GST ({row['gst']}%):** ₹{gst_amount:.2f} = **₹{item_total:.2f}**")
        
            selected_items = []
            for item_id, qty in st.session_state['selected_quantities'].items():
                if qty > 0:
                    item_details = menu_items_df[menu_items_df['item_id'] == item_id].iloc[0]
                    base_total = float(item_details['price']) * int(qty)
                    gst_amount = base_total * float(item_details['gst']) / 100.0
                    item_total = base_total + gst_amount
                    selected_items.append({
                        "item_id": int(item_id),
                        "name": str(item_details['item_name']),
                        "qty": int(qty),
                        "unit_price": float(item_details['price']),
                        "gst": float(item_details['gst']),
                        "gst_amount": round(gst_amount, 2),
                        "total": round(item_total, 2),
                    })

            if selected_items:
                st.subheader("🧾 Order Summary")
                for item in selected_items:
                    st.write(f"{item['name']} x {item['qty']} = ₹{item['total']} (incl. ₹{item['gst_amount']} GST)")
                grand_total = sum(item["total"] for item in selected_items)
                
                st.markdown("---")
                discount_pct = st.number_input("💸 Enter Discount % (if any)", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key='discount_input')
                discount_amount = grand_total * discount_pct / 100.0
                total_after_discount = grand_total - discount_amount
                tip_pct = st.number_input("💰 Enter Tip % (optional)", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key='tip_input')
                tip_amount = total_after_discount * tip_pct / 100.0
                final_total = total_after_discount + tip_amount
                
                st.markdown(f"### 💵 Total before discount: ₹{grand_total:.2f}")
                st.markdown(f"### 🔖 Discount ({discount_pct}%): -₹{discount_amount:.2f}")
                st.markdown(f"### 💸 Tip ({tip_pct}%): +₹{tip_amount:.2f}")
                st.markdown(f"### 💰 Total Payable: ₹{final_total:.2f}")
                
                st.markdown("---")
                st.subheader("💳 Select Payment Method")
                
                col_cash, col_card, col_upi = st.columns(3)
                with col_cash:
                    if st.button("Pay with Cash", use_container_width=True, key="pay_cash_button"):
                        st.session_state['payment_method_selected'] = "Cash"
                with col_card:
                    if st.button("Pay with Card", use_container_width=True, key="pay_card_button"):
                        st.session_state['payment_method_selected'] = "Card"
                with col_upi:
                    if st.button("Pay with UPI", use_container_width=True, key="pay_upi_button"):
                        st.session_state['payment_method_selected'] = "UPI"
                
                if st.session_state['payment_method_selected'] == "UPI" and not st.session_state['is_order_submitted']:
                    st.info("Scan the QR code to pay with UPI")
                    try:
                        qr_img = generate_upi_qr_code(final_total)
                        st.image(pil_to_bytes(qr_img), width=250, caption="Scan to Pay")
                    except Exception as e:
                        st.error(f"Error generating QR code: {e}")
                    
                    st.markdown("---")
                    
                    if st.button("Confirm UPI Payment", key="confirm_upi_payment"):
                        st.session_state['is_order_submitted'] = True
                        st.session_state['payment_method'] = "UPI"
                
                elif st.session_state['payment_method_selected'] == "Card":
                    st.info("Simulating card payment...")
                    with st.spinner('Processing payment...'):
                        time.sleep(2)
                    st.success("Card payment successful!")
                    if st.button("Finalize Order", key="finalize_card_payment"):
                        st.session_state['is_order_submitted'] = True
                        st.session_state['payment_method'] = "Card"
                
                elif st.session_state['payment_method_selected'] == "Cash":
                    st.info("Waiting for cash payment...")
                    if st.button("Confirm Cash Payment", key="confirm_cash_payment"):
                        st.session_state['is_order_submitted'] = True
                        st.session_state['payment_method'] = "Cash"

                if st.session_state['is_order_submitted']:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
                    order_data = {
                        "mode": order_mode,
                        "payment": st.session_state['payment_method'],
                        "timestamp": timestamp,
                        "total": round(final_total, 2),
                        "items": selected_items,
                    }
        
                    try:
                        order_id = save_order_to_db(order_data)
                        st.session_state['success_message'] = f"🧾 Order #{order_id} submitted and saved successfully!"
                        st.session_state['last_order_id'] = order_id
                        
                        st.session_state['is_order_submitted'] = False
                        st.session_state['payment_method_selected'] = None
                        st.cache_data.clear()
                        st.rerun()
        
                    except Exception as e:
                        st.error(f"Error saving order: {e}")
                        st.code(traceback.format_exc())


    # ----------------- Menu Management Page -----------------
    elif page == "Menu Management":
        st.title("👨‍🍳 Menu Management")
        st.markdown("Use this page to add, edit, or delete menu items. Changes are saved directly to the database.")

        st.subheader("Add / Edit Menu Item")

        menu_df = get_menu_items()
        edit_item = None
        if st.session_state['edit_item_id']:
            edit_items_filtered = menu_df[menu_df['item_id'] == st.session_state['edit_item_id']]
            if not edit_items_filtered.empty:
                edit_item = edit_items_filtered.iloc[0]
            else:
                st.session_state['edit_item_id'] = None
                st.warning("Selected item for editing was not found. Please select an existing item.")


        with st.form("menu_item_form", clear_on_submit=True):
            item_name = st.text_input("Item Name", value=edit_item['item_name'] if edit_item is not None else "", key='item_name_input')
            category = st.text_input("Category", value=edit_item['category'] if edit_item is not None else "", key='category_input')
            price = st.number_input("Price (₹)", min_value=0.0, step=0.5, value=float(edit_item['price']) if edit_item is not None else 0.0, key='price_input')
            gst = st.number_input("GST %", min_value=0.0, max_value=100.0, step=0.5, value=float(edit_item['gst']) if edit_item is not None else 5.0, key='gst_input')
            image_url = st.text_input("Image URL", value=edit_item['image_url'] if edit_item is not None else "https://placehold.co/100x100/600/fff?text=No+Image", key='image_url_input')

            submit_button = st.form_submit_button("Save Item")

            if submit_button:
                if not item_name.strip():
                    st.error("Item Name cannot be empty.")
                elif not category.strip():
                    st.error("Category cannot be empty.")
                elif price < 0:
                    st.error("Price cannot be negative.")
                elif gst < 0:
                    st.error("GST cannot be negative.")
                else:
                    if st.session_state['edit_item_id']:
                        update_menu_item_in_db(st.session_state['edit_item_id'], item_name, category, price, gst, image_url)
                        st.session_state['edit_item_id'] = None
                    else:
                        add_menu_item_to_db(item_name, category, price, gst, image_url)

        st.markdown("---")

        st.subheader("Current Menu Items")

        menu_items = get_menu_items()
        if menu_items.empty:
            st.info("No menu items found. Add one using the form above.")
        else:
            header_cols = st.columns([0.5, 3, 1, 1, 1, 1, 1])
            header_cols[0].markdown("**ID**")
            header_cols[1].markdown("**Item Name**")
            header_cols[2].markdown("**Category**")
            header_cols[3].markdown("**Price**")
            header_cols[4].markdown("**GST %**")
            header_cols[5].markdown("**Edit**")
            header_cols[6].markdown("**Delete**")
            
            st.markdown("---")

            for index, row in menu_items.iterrows():
                cols = st.columns([0.5, 3, 1, 1, 1, 1, 1])

                item_id = row['item_id']
                item_name = row['item_name']
                category = row['category']
                price = row['price']
                gst = row['gst']
                image_url = row['image_url']

                with cols[0]:
                    st.write(item_id)
                with cols[1]:
                    st.write(item_name)
                with cols[2]:
                    st.write(category)
                with cols[3]:
                    st.write(f"₹{price:.2f}")
                with cols[4]:
                    st.write(f"{gst:.1f}%")

                with cols[5]:
                    if st.button("✏️ Edit", key=f"edit_{item_id}", use_container_width=True):
                        st.session_state['edit_item_id'] = item_id
                        st.rerun()
                with cols[6]:
                    if st.button("❌ Delete", key=f"delete_{item_id}", use_container_width=True):
                        delete_menu_item_from_db(item_id)
                st.markdown("---")


    # ----------------- Order History  -----------------
    elif page == "Order History":
        st.title("🕘 Order History")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=7), key="history_start_date")
        with col2:
            end_date = st.date_input("End Date", value=datetime.date.today(), key="history_end_date")
        
        orders_df = get_orders(start_date=start_date, end_date=end_date)
        
        if orders_df.empty:
            st.info("No orders found for the selected period.")
        else:
            st.subheader("📋 Filtered Order Details")
            st.write(f"Showing {len(orders_df)} orders from {start_date} to {end_date}")
            menu_dict_full = get_menu_dict()
            
            all_orders_data = []

            for _, order in orders_df.iterrows():
                with st.expander(
                    f"Order #{order['order_id']} | {order['mode']} | {order['payment']} | ₹{order['total']:.2f}"
                ):
                    st.write(f"Timestamp: {order['timestamp']}")
                    items_raw = get_order_items(int(order['order_id']))
                    
                    order_items_for_display = []
                    subtotal_before_gst = 0
                    gst_amount = 0
                    
                    for item_id, qty, total_item_with_gst in items_raw:
                        item_name = menu_dict_full.get(item_id, {}).get("item_name", f"Item {item_id}")
                        unit_price = menu_dict_full.get(item_id, {}).get("price", 0)

                        base_total_for_item = unit_price * qty
                        gst_for_item = total_item_with_gst - base_total_for_item
                        
                        subtotal_before_gst += base_total_for_item
                        gst_amount += gst_for_item
                        
                        order_items_for_display.append({
                            "Item Name": item_name,
                            "Qty": qty,
                            "Unit Price": unit_price,
                            "Item Total": total_item_with_gst
                        })

                        all_orders_data.append({
                            "Order ID": order['order_id'],
                            "Timestamp": order['timestamp'],
                            "Mode": order['mode'],
                            "Payment": order['payment'],
                            "Item Name": item_name,
                            "Qty": qty,
                            "Unit Price": unit_price,
                            "Total (with GST)": total_item_with_gst,
                            "Order Total": order['total']
                        })
                    
                    st.dataframe(pd.DataFrame(order_items_for_display), use_container_width=True, hide_index=True)
                    st.markdown(f"**Order Total:** ₹{order['total']:.2f}")

            if not orders_df.empty:
                full_export_df = pd.DataFrame(all_orders_data)
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    full_export_df.to_excel(writer, sheet_name='Order History', index=False)
                
                st.download_button(
                    label="📥 Download Order History (Excel)",
                    data=output.getvalue(),
                    file_name=f"order_history_{start_date}_to_{end_date}.xlsx",
                    mime="application/vnd.ms-excel"
                )

    # ----------------- Analytics Dashboard -----------------
    elif page == "Analytics Dashboard":
        st.title("📈 Analytics Dashboard")
        st.markdown("View key metrics and trends for your restaurant.")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30), key="analytics_start_date")
        with col2:
            end_date = st.date_input("End Date", value=datetime.date.today(), key="analytics_end_date")
        
        total_revenue = get_total_revenue(start_date, end_date)
        num_orders = get_num_orders(start_date, end_date)
        
        col_rev, col_orders, col_avg = st.columns(3)
        with col_rev:
            st.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")
        with col_orders:
            st.metric(label="Total Orders", value=num_orders)
        with col_avg:
            avg_order_value = total_revenue / num_orders if num_orders > 0 else 0
            st.metric(label="Avg. Order Value", value=f"₹{avg_order_value:,.2f}")

        st.markdown("---")
        
        st.subheader("Daily Sales Trend")
        sales_by_date_df = get_sales_by_date(start_date, end_date)
        if not sales_by_date_df.empty:
            if plotly_available:
                fig_daily_sales = px.line(sales_by_date_df, x='order_date', y='daily_sales', markers=True, title="Daily Sales")
                fig_daily_sales.update_layout(xaxis_title="Date", yaxis_title="Daily Sales (₹)")
                st.plotly_chart(fig_daily_sales, use_container_width=True)
            else:
                st.line_chart(sales_by_date_df, x='order_date', y='daily_sales')
        else:
            st.info("No daily sales data for the selected period.")

        st.markdown("---")

        col_charts_1, col_charts_2 = st.columns(2)
        with col_charts_1:
            st.subheader("Sales by Payment Method")
            sales_by_payment_df = get_sales_by_payment_method(start_date, end_date)
            if not sales_by_payment_df.empty:
                if plotly_available:
                    fig_payment = px.pie(sales_by_payment_df, values='total_sales', names='payment', title='Sales by Payment Method')
                    st.plotly_chart(fig_payment, use_container_width=True)
                else:
                    st.dataframe(sales_by_payment_df, use_container_width=True, hide_index=True)
            else:
                st.info("No payment method data for the selected period.")

        with col_charts_2:
            st.subheader("Sales by Category")
            sales_by_category_df = get_sales_by_category(start_date, end_date)
            if not sales_by_category_df.empty:
                if plotly_available:
                    fig_category = px.bar(sales_by_category_df, x='category', y='total_sales', title='Sales by Category')
                    fig_category.update_layout(xaxis_title="Category", yaxis_title="Total Sales (₹)")
                    st.plotly_chart(fig_category, use_container_width=True)
                else:
                    st.bar_chart(sales_by_category_df, x='category', y='total_sales')
            else:
                st.info("No category sales data for the selected period.")

        st.markdown("---")
        
        st.subheader("Top 5 Most Sold Items")
        most_sold_items = get_most_sold_items(start_date, end_date, top_n=5)
        if most_sold_items:
            most_sold_df = pd.DataFrame(most_sold_items, columns=["Item Name", "Total Quantity Sold"])
            if plotly_available:
                fig_top_items = px.bar(most_sold_df, x='Total Quantity Sold', y='Item Name', orientation='h', title='Top 5 Most Sold Items')
                st.plotly_chart(fig_top_items, use_container_width=True)
            else:
                st.bar_chart(most_sold_df.set_index('Item Name'))
        else:
            st.info("No sales data available to determine most sold items.")