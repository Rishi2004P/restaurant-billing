def calculate_item_total(price, gst, qty):
    """
    Calculates the total for a single item, including GST.
    
    Args:
        price (float): The unit price of the item.
        gst (float): The GST percentage.
        qty (int): The quantity of the item.
        
    Returns:
        tuple: A tuple containing the base total, GST amount, and total with GST.
    """
    base_total = price * qty
    gst_amount = base_total * (gst / 100.0)
    item_total = base_total + gst_amount
    return base_total, gst_amount, item_total


def calculate_order_summary(selected_items, discount_pct, tip_pct):
    """
    Calculates the complete summary for an order, including totals, discounts, and tips.
    
    Args:
        selected_items (list): A list of dictionaries, where each dictionary
                               represents a selected item and its calculated details.
        discount_pct (float): The discount percentage to apply.
        tip_pct (float): The tip percentage to apply.
        
    Returns:
        dict: A dictionary containing the subtotal, grand total, discount amount,
              tip amount, and the final payable amount.
    """
    grand_total_before_discount = sum(item["total"] for item in selected_items)
    
    discount_amount = grand_total_before_discount * (discount_pct / 100.0)
    total_after_discount = grand_total_before_discount - discount_amount
    
    tip_amount = total_after_discount * (tip_pct / 100.0)
    final_total = total_after_discount + tip_amount
    
    return {
        "subtotal": grand_total_before_discount,
        "discount_amount": discount_amount,
        "tip_amount": tip_amount,
        "final_total": final_total,
    }
