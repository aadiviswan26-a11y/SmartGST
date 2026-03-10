# backend/category_rules.py
"""
Simple rule-based category detector for GST slabs.
This is intentionally straightforward and deterministic so your app
can auto-detect GST slab from a product description.
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

# quick mapping rate -> readable name
RATE_TO_CATEGORY_NAME = {c["rate"]: c["name"] for c in GST_CATEGORIES}


def auto_detect_slab(product):
    """
    Given a product string, try:
      1) direct substring match against keywords.
      2) fuzzy match against all keywords (threshold 70).
    Returns a GST rate (int). Falls back to DEFAULT_GST_RATE.
    """
    if not product:
        return DEFAULT_GST_RATE

    prod = product.lower()

    # direct substring match - fast and deterministic
    for cat in GST_CATEGORIES:
        for kw in cat["keywords"]:
            if kw in prod:
                return cat["rate"]

    # fuzzy match over all keywords
    try:
        all_keywords = [kw for c in GST_CATEGORIES for kw in c["keywords"]]
        best_match = None
        best_score = 0
        
        for kw in all_keywords:
            score = fuzz.ratio(prod, kw)
            if score > best_score:
                best_score = score
                best_match = kw
        
        if best_score >= 70:
            # find corresponding category
            for cat in GST_CATEGORIES:
                if best_match in cat["keywords"]:
                    return cat["rate"]
    except Exception:
        # rapidfuzz might throw if unexpected input - fallback
        pass

    return DEFAULT_GST_RATE
