import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime

# --- PDF Generation Function ---
def generate_pdf_bill(order_id, order_items, subtotal, gst, discount, total, payment_method, mode):
    """
    Generates a professional-looking PDF bill with detailed information.
    
    Args:
        order_id (int): The unique ID of the order.
        order_items (list): A list of dictionaries, each containing 'item', 'qty',
                            'price', and 'total' for an item.
        subtotal (float): The total price of items before discounts and GST.
        gst (float): The total GST amount.
        discount (float): The total discount amount.
        total (float): The final payable amount.
        payment_method (str): The method of payment (e.g., 'Cash', 'Card').
        mode (str): The order mode (e.g., 'Dine-In', 'Takeaway').
        
    Returns:
        bytes: The binary data of the generated PDF file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom style for right-aligned text
    styles.add(ParagraphStyle(name='RightAlign', alignment=2)) # 2 means right alignment
    
    story = []

    # --- Header with Business Info ---
    # Restaurant name and address
    story.append(Paragraph(
        "<font size='18'><b>Imperial Spice</b></font>",
        styles['Heading1']
    ))
    story.append(Paragraph("123, Food Street, Gourmet City", styles['Normal']))
    story.append(Paragraph("Email: contact@restaurant.com | Phone: +91 98765 43210", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # --- Bill Title and Details ---
    styles.add(ParagraphStyle(name='TitleStyle', alignment=1, fontSize=16, fontName='Helvetica-Bold'))
    story.append(Paragraph(f"<b>TAX INVOICE</b>", styles['TitleStyle']))
    story.append(Spacer(1, 0.1 * inch))
    
    # Use a table for clean layout of order details
    details_data = [
        ["Order ID:", f"#{order_id}"],
        ["Order Date:", datetime.datetime.now().strftime("%Y-%m-%d")],
        ["Order Time:", datetime.datetime.now().strftime("%H:%M:%S")],
        ["Order Mode:", mode],
        ["Payment Method:", payment_method]
    ]
    details_table = Table(details_data, colWidths=[2 * inch, 5 * inch])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ('BOX', (0, 0), (-1, -1), 0, colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkgrey),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.2 * inch))

    # --- Items Table ---
    data = [['Item', 'Qty', 'Unit Price', 'Total']]
    for item in order_items:
        data.append([item['item'], str(item['qty']), f"₹{item['price']:.2f}", f"₹{item['total']:.2f}"])

    item_table = Table(data, colWidths=[3 * inch, 0.7 * inch, 1.5 * inch, 1.5 * inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 0.1 * inch))
    
    # --- Horizontal line for visual separation ---
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceAfter=12, spaceBefore=12))

    # --- Summary Section with improved alignment ---
    story.append(Table(
        [[Paragraph("Subtotal:", styles['Normal']), Paragraph(f"₹{subtotal:.2f}", styles['RightAlign'])]],
        colWidths=[5 * inch, 2 * inch],
        style=[('BOX', (0, 0), (-1, -1), 0, colors.white), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
    ))
    story.append(Table(
        [[Paragraph("GST:", styles['Normal']), Paragraph(f"₹{gst:.2f}", styles['RightAlign'])]],
        colWidths=[5 * inch, 2 * inch],
        style=[('BOX', (0, 0), (-1, -1), 0, colors.white), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
    ))
    story.append(Table(
        [[Paragraph("Discount:", styles['Normal']), Paragraph(f"-₹{discount:.2f}", styles['RightAlign'])]],
        colWidths=[5 * inch, 2 * inch],
        style=[('BOX', (0, 0), (-1, -1), 0, colors.white), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
    ))
    story.append(Table(
        [[Paragraph("<b>TOTAL PAYABLE:</b>", styles['Normal']), Paragraph(f"<b>₹{total:.2f}</b>", styles['RightAlign'])]],
        colWidths=[5 * inch, 2 * inch],
        style=[('BOX', (0, 0), (-1, -1), 0, colors.white), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
    ))

    story.append(Spacer(1, 0.5 * inch))
    
    # --- Footer ---
    story.append(Paragraph("Thank you for your visit!", styles['Normal']))
    story.append(Paragraph("For any queries, please contact us.", styles['Normal']))

    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

if __name__ == '__main__':
    # This is a sample usage to demonstrate the function
    
    sample_order_items = [
        {'item': 'Green Salad', 'qty': 2, 'price': 80.0, 'total': 168.0},
        {'item': 'Cucumber Raita', 'qty': 1, 'price': 90.0, 'total': 94.5},
        {'item': 'Boondi Raita', 'qty': 3, 'price': 95.0, 'total': 299.25},
    ]
    
    sample_subtotal = sum(item['price'] * item['qty'] for item in sample_order_items)
    sample_gst = sum(item['total'] - (item['price'] * item['qty']) for item in sample_order_items)
    sample_discount = 20.0
    sample_total = sample_subtotal + sample_gst - sample_discount
    
    pdf_data = generate_pdf_bill(
        order_id=123,
        order_items=sample_order_items,
        subtotal=sample_subtotal,
        gst=sample_gst,
        discount=sample_discount,
        total=sample_total,
        payment_method="UPI",
        mode="Dine-In"
    )
    
    with open("sample_receipt.pdf", "wb") as f:
        f.write(pdf_data)
    print("Sample PDF receipt 'sample_receipt.pdf' has been generated.")