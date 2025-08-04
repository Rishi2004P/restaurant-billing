# 🍽️ Restaurant Billing System: Internship Project

## 🚀 Project Overview

This project is a modern, Python-based billing system designed specifically for restaurants. Built with the powerful **Streamlit** framework for the user interface and backed by an **SQLite3** database for data persistence, the application provides a robust and user-friendly solution for managing orders, generating bills, and analyzing sales data.

---

## ✨ Key Features

### 🔒 User Authentication
- Secure login functionality with distinct roles for **admin** and **cashier**.

### 📝 Order Management
- Choose between **Dine-In** and **Takeaway** modes.
- Browse an interactive menu, categorized for easy ordering.
- Effortlessly add, remove, and adjust quantities of items.

### 💰 Billing & Calculations
- Automatic calculation of **subtotal**, **GST**, and **optional discounts**.
- Supports multiple payment methods: **Cash**, **Card**, **UPI** (with a QR code).
- Real-time bill summary with detailed item breakdown.

### 🖨️ Bill Generation
- Generate and download the final receipt in **PDF** and **CSV** formats.

### 💾 Data Storage
- All orders and menu items stored in **restaurant.db** using SQLite3.

### 📈 Reporting & Analytics
- Dashboard for **daily**, **weekly**, and **monthly** sales reports.
- Key KPIs: **Total Revenue**, **Order Count**, **Average Order Value**.
- Most sold items are identified and ranked.

### ⚙️ Menu Management (Admin Only)
- Add, edit, or delete menu items from the app directly.
- Includes image URL support for each item.

---

## 🛠️ Technology Stack

| Component           | Technology     |
|---------------------|----------------|
| Backend & Logic     | Python         |
| Web Interface       | Streamlit      |
| Database            | SQLite3        |
| Data Handling       | Pandas         |
| PDF Generation      | FPDF           |
| QR Code Generator   | qrcode         |
| Charts              | Plotly         |

---

## 🚀 How to Set Up and Run the Project

### 1. Prerequisites
Ensure Python 3.8 or above is installed on your system.

### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd restaurant-billing

3. Install Dependencies

pip install -r requirements.txt

Sample requirements.txt:
streamlit
pandas
sqlite3
fpdf
qrcode
Pillow
plotly
xlsxwriter

Project Structure

RESTAURANT_BILLING/
├── .dist/
├── data/
├── db/
├── receipts/
├── scripts/
├── ui/
│   ├── main_ui.py              # ✅ Main app entry point
│   └── restaurant.db
├── utils/
├── venv/
├── .gitignore
├── app.py                      # (Not primary)
├── download_fonts.py
├── main.py
├── README.md
└── test_fpdf2_import.py

Run the Application

streamlit run ui/main_ui.py
A local development server will start. Access the app through the provided local URL (usually http://localhost:8501).

| Role    | Username | Password    |
| ------- | -------- | ----------- |
| Admin   | admin    | password123 |
| Cashier | cashier  | cashierpass |

Database Schema
The database restaurant.db contains the following tables:

menu:
item_id, item_name, category, price, gst, image_url

orders:
order_id, mode, payment, timestamp, total

order_items:
item_id, order_id, qty, total

