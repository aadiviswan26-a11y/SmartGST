# backend/category_rules.py
"""
Improved rule-based category detector for GST slabs.

Fixes:
- Prevents incorrect 0% matches (like "water bottle")
- Uses stricter word matching instead of loose substring
- Better fuzzy matching with higher accuracy
- Prioritizes longer and more specific keywords
"""

from rapidfuzz import fuzz

DEFAULT_GST_RATE = 18

GST_CATEGORIES = [
    {
        "name": "Essential Goods (0%)",
        "rate": 0,
        "keywords": [
            "fresh vegetables", "fresh fruits", "vegetables", "fruits",
            "milk", "curd", "lassi", "buttermilk",
            "eggs", "egg", "fish", "meat",
            "rice", "wheat", "flour", "atta", "maida", "besan",
            "grains", "cereals", "dal",
            "education", "school", "tuition",
            "books", "notebooks", "pencil", "eraser", "map", "chart",
            "globe", "exercise book",
            "hospital", "doctor", "healthcare", "medicine", "life saving",
            "health insurance", "life insurance",
            "honey", "drinking water",
            "sanitary napkin", "sanitary pads"
        ]
    },

    {
        "name": "Merit Goods (5%)",
        "rate": 5,
        "keywords": [
            "packaged food", "namkeen", "biscuits", "biscuit",
            "pasta", "noodles", "ready to eat", "ready to cook",
            "butter", "ghee", "cheese",
            "hair oil", "shampoo", "soap", "toothpaste",
            "toothbrush", "detergent", "utensils",
            "footwear", "shoes", "clothes", "dress", "shirt",
            "tablet", "capsule", "syrup",
            "thermometer", "oxygen cylinder",
            "medical oxygen", "diagnostic kit",
            "hotel stay", "gym service",
            "fitness centre", "spa",
            "ready meals", "snacks", "chocolate", "ice cream",
            "cooking oil", "salt", "spices"
        ]
    },

    {
        "name": "Standard Goods & Services (18%)",
        "rate": 18,
        "keywords": [
            "air conditioner", "ac", "refrigerator", "fridge",
            "television", "tv", "smart tv", "washing machine",
            "printer", "scanner", "microwave", "mixer", "grinder",
            "fan", "cooler", "geyser",
            "mobile", "smartphone", "laptop", "computer",
            "keyboard", "mouse", "smartwatch",
            "power bank", "router", "modem",
            "cement", "steel", "construction material",
            "car", "hatchback", "sedan", "bike", "motorcycle",
            "it service", "software service", "legal service",
            "accounting service", "consultancy service",
            "internet service", "wifi", "broadband",
            "mineral water", "school bag", "premium stationery"
        ]
    },

    {
        "name": "Luxury & Sin Goods (40%)",
        "rate": 40,
        "keywords": [
            "luxury car", "premium car", "sports car",
            "superbike", "motorcycle above 350cc",
            "yacht", "aircraft", "jet",
            "tobacco", "cigarette", "pan masala",
            "aerated drink", "energy drink",
            "sugary drink", "caffeinated drink",
            "casino", "gambling", "betting", "horse racing",
            "perfume", "designer perfume"
        ]
    }
]

# mapping
RATE_TO_CATEGORY_NAME = {c["rate"]: c["name"] for c in GST_CATEGORIES}


def clean_text(text):
    """Normalize text for better matching"""
    return f" {text.lower().strip()} "


def auto_detect_slab(product):
    """
    Improved detection:
    1. Exact + word-boundary match (prevents wrong matches like 'water bottle')
    2. Longer keywords prioritized
    3. Safer fuzzy matching (high threshold)
    """

    if not product:
        return DEFAULT_GST_RATE

    prod = clean_text(product)

    # -------- STEP 1: STRICT MATCH (word boundary safe) --------
    for cat in GST_CATEGORIES:
        # sort keywords by length (longer first = more accurate)
        keywords = sorted(cat["keywords"], key=len, reverse=True)

        for kw in keywords:
            kw_clean = clean_text(kw)

            # exact phrase match with boundaries
            if kw_clean in prod:
                return cat["rate"]

    # -------- STEP 2: FUZZY MATCH (controlled) --------
    best_score = 0
    best_rate = DEFAULT_GST_RATE

    try:
        for cat in GST_CATEGORIES:
            for kw in cat["keywords"]:
                score = fuzz.token_set_ratio(product.lower(), kw)

                if score > best_score:
                    best_score = score
                    best_rate = cat["rate"]

        # ✅ HIGH threshold to avoid wrong matches
        if best_score >= 85:
            return best_rate

    except Exception:
        pass

    # -------- FALLBACK --------
    return DEFAULT_GST_RATE