# backend/gst_engine.py
from backend.category_rules import auto_detect_slab, RATE_TO_CATEGORY_NAME
from backend.history_manager import save_history

def gst_calculation(product, price, gst_type="exclusive", gst_category="cgst_sgst"):
    """
    Calculate GST for a product & price.
    - gst_type: "exclusive" => price is base (add GST)
                "inclusive" => price already includes GST
    - gst_category currently not used for separate math, kept for UI clarity.
    Returns: (rate, gst_amount, final_price, category_name)
    """
    rate = auto_detect_slab(product)

    # Exclusive GST: price is base price
    if gst_type == "exclusive":
        gst_amount = round(price * rate / 100, 2)
        final_price = round(price + gst_amount, 2)
        base_price_for_history = price

    # Inclusive GST: price already includes GST
    else:
        total_price = price
        base_price = total_price / (1 + rate / 100)
        base_price = round(base_price, 2)
        gst_amount = round(total_price - base_price, 2)
        final_price = round(total_price, 2)
        base_price_for_history = base_price

    # Save history (use base price for history when inclusive)
    try:
        save_history(product, base_price_for_history, rate, gst_amount, final_price)
    except Exception as e:
        # don't crash the calculation if history save fails; log to stdout for debugging
        print("Warning: failed to save history:", e)

    category_name = RATE_TO_CATEGORY_NAME.get(rate, f"{rate}% slab")
    return rate, gst_amount, final_price, category_name
