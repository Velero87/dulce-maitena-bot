import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Dulce Maitena")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    META_GRAPH_VERSION = os.getenv("META_GRAPH_VERSION", "v25.0")
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5000")

    DEFAULT_IMAGE_PATH = os.getenv("DEFAULT_IMAGE_PATH", "content/images/alfajor_1.jpg")
    AUTO_POST_HOUR = int(os.getenv("AUTO_POST_HOUR", "10"))
    AUTO_POST_MINUTE = int(os.getenv("AUTO_POST_MINUTE", "0"))
    TIMEZONE = os.getenv("TIMEZONE", "America/Argentina/San_Luis")

    ORDER_CATALOG_URL = os.getenv("ORDER_CATALOG_URL", "https://wa.me/5490000000000")
    WHATSAPP_NUMBER_DISPLAY = os.getenv("WHATSAPP_NUMBER_DISPLAY", "+54 9 XXX XXX XXXX")
    DEFAULT_CITY = os.getenv("DEFAULT_CITY", "San Luis")
    ENABLE_INSTAGRAM_AUTO_REPLY = os.getenv("ENABLE_INSTAGRAM_AUTO_REPLY", "false").lower() == "true"

    WHATSAPP_AI_ENABLED = os.getenv("WHATSAPP_AI_ENABLED", "true").lower() == "true"
    HUMAN_HANDOFF_KEYWORDS = [
        x.strip().lower() for x in os.getenv(
            "HUMAN_HANDOFF_KEYWORDS",
            "humano,persona,asesor,pago,transferencia,comprobante,urgente"
        ).split(",") if x.strip()
    ]
    ORDER_PRICE_6 = os.getenv("ORDER_PRICE_6", "")
    ORDER_PRICE_12 = os.getenv("ORDER_PRICE_12", "")
    ORDER_PAYMENT_METHODS = os.getenv("ORDER_PAYMENT_METHODS", "Efectivo o transferencia")
    WHATSAPP_TEMPLATE_RESUME = os.getenv("WHATSAPP_TEMPLATE_RESUME", "")


settings = Settings()
