# backend/fraud_detector.py
def check_fraud(final_amount, billed):
    """
    Compare final_amount (calculated) vs billed (amount customer paid).
    Returns a simple human-readable message.
    """
    try:
        final_amount = float(final_amount)
        billed = float(billed)
    except Exception:
        return "Invalid numeric values provided."

    diff = round(billed - final_amount, 2)
    if abs(diff) < 0.01:
        return "Shop billed correctly."
    elif diff > 0:
        return f"Shop charged extra ₹{diff:.2f}."
    else:
        return f"Shop undercharged by ₹{abs(diff):.2f}."
