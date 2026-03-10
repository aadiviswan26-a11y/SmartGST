# backend/history_manager.py
import csv
import os
from datetime import datetime

# database directory placed next to project root (one level up from backend/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(BASE_DIR, "database")
FILE_NAME = os.path.join(DB_DIR, "gst_history.csv")

# ensure database folder exists
os.makedirs(DB_DIR, exist_ok=True)


def save_history(product, price, rate, gst_amount, final_price):
    """
    Append a row to the GST history CSV. Creates file with header if missing.
    """
    exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["Time", "Product", "Price", "GST%", "GST Amount", "Total"])
        w.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product, price, rate, gst_amount, final_price
        ])


def read_history():
    """
    Return list of rows (excluding header). Each row is a list of strings.
    If file missing or only header -> return [].
    """
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        rows = list(r)
        if not rows:
            return []
        # if header present, skip it
        if rows[0] and rows[0][0].lower().startswith("time"):
            return rows[1:]
        return rows
