import os
import sqlite3
import pandas as pd
import requests  # Required to validate image URLs

# Path to your database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "orders.db")

def init_db():
    """
    Initializes the SQLite database with the orders table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            order_mode TEXT,
            items TEXT,
            total_amount REAL,
            payment_method TEXT
        )
    ''')
    conn.commit()
    conn.close()

def sanitize_menu_image_urls():
    """
    Checks if image URLs in menu.csv are valid.
    If not, replaces them with a placeholder image.
    """
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "menu.csv")
    placeholder_image = "https://placehold.co/100x100/600/fff?text=No+Image"

    df = pd.read_csv(csv_path)
    updated = False

    for index, row in df.iterrows():
        image_url = str(row.get("image_url", "")).strip()

        if image_url.startswith("http"):
            try:
                response = requests.head(image_url, timeout=3)
                if response.status_code >= 400:
                    df.at[index, "image_url"] = placeholder_image
                    updated = True
            except:
                df.at[index, "image_url"] = placeholder_image
                updated = True
        else:
            df.at[index, "image_url"] = placeholder_image
            updated = True

    if updated:
        df.to_csv(csv_path, index=False)

def load_menu_from_csv():
    """
    Loads and sanitizes menu items from menu.csv.
    Returns a list of dicts.
    """
    sanitize_menu_image_urls()
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "menu.csv")
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

def save_order_to_db(timestamp, order_mode, items, total_amount, payment_method):
    """
    Saves an order to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (timestamp, order_mode, items, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, order_mode, str(items), total_amount, payment_method))
    conn.commit()
    conn.close()

def get_orders():
    """
    Retrieves all past orders from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows