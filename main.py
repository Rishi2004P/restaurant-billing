import os
import sys

# Get the absolute path of the directory containing this script.
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the 'utils' directory.
utils_path = os.path.join(current_dir, 'utils')

# Add the 'utils' directory to the Python search path.
# This makes it a top-level location for imports, so 'pdf_generator' and 'download_fonts'
# can be imported as if they were in the same directory as main.py.
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

# Now, we can import from the 'pdf_generator' module directly.
try:
    from pdf_generator import generate_pdf_bill
except ImportError as e:
    print(f"Error importing pdf_generator: {e}")
    print("Please ensure you are running this script from the 'restaurant_billing' folder.")
    sys.exit(1)

# =========================================================================
# TODO: REPLACE THIS EXAMPLE DATA WITH YOUR ACTUAL MENU AND ORDER LOGIC.
# This section is for you to integrate with your application's data.
# =========================================================================

# This is a sample order. You should generate these values from your application.
# For example, from a user's cart or a database.
order_id = 12345
order_items_data = [
    {"item": "Your Menu Item 1", "qty": 1, "price": 200.0, "total": 200.0},
    {"item": "Your Menu Item 2", "qty": 2, "price": 100.0, "total": 200.0},
]
subtotal = 400.0
gst = 40.0
discount = 0.0
total = 440.0
payment_method = "Card"
mode = "Dine-In"

# =========================================================================
# END OF EXAMPLE DATA
# =========================================================================

# Call the function to generate the PDF bill with your order data.
generate_pdf_bill(
    order_id=order_id,
    order_items=order_items_data,
    subtotal=subtotal,
    gst=gst,
    discount=discount,
    total=total,
    payment_method=payment_method,
    mode=mode
)

print("PDF bill generated successfully!")
print(f"Look for 'order_{order_id}.pdf' in the 'restaurant_billing/receipts' directory.")