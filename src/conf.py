import os

class Settings:
    port: int = 8000
    host: str = "127.0.0.1"

    price_100g: float = float(os.getenv("PRICE_100G", 160))  # price per 100 grams
    price_100g_discounted: float = float(os.getenv("PRICE_100G_DISCOUNTED", 150))  # discounted price per 100 grams
    discount_threshold_grams: float = float(os.getenv("DISCOUNT_THRESHOLD_GRAMS", 650))  # threshold grams for discount




settings = Settings()
