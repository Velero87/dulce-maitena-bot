from app.config import settings
from app.db import get_recent_messages, get_state, log_message, upsert_state
from app.services.claude_service import generate_whatsapp_reply


WELCOME_TEXT = f"""¡Hola! 👋
Gracias por escribir a {settings.BUSINESS_NAME} 💛
Decime si querés precio, envío o hacer un pedido.
Si querés comprar, pasame cantidad y zona."""

HUMAN_TEXT = f"""Perfecto 💛
Tu consulta necesita atención humana.
En breve te respondemos desde {settings.BUSINESS_NAME}.
Si querés adelantar, pasanos cantidad, zona y forma de pago."""

NON_TEXT_TEXT = "Gracias por escribirnos 💛 Por ahora solo puedo responder mensajes de texto. Decime qué necesitás y te ayudo."



def should_handoff_to_human(message_text: str) -> bool:
    text = (message_text or "").lower().strip()
    return any(word in text for word in settings.HUMAN_HANDOFF_KEYWORDS)



def handle_whatsapp_message(user_id: str, message_text: str) -> str:
    text = (message_text or "").strip()
    if not text:
        return NON_TEXT_TEXT

    log_message("whatsapp", user_id, "user", text)

    if should_handoff_to_human(text):
        upsert_state("whatsapp", user_id, "human_handoff", text)
        log_message("whatsapp", user_id, "assistant", HUMAN_TEXT)
        return HUMAN_TEXT

    state = get_state("whatsapp", user_id)
    if state is None and text.lower() in {"hola", "buenas", "buen dia", "buen día", "hello"}:
        upsert_state("whatsapp", user_id, "greeting", text)
        log_message("whatsapp", user_id, "assistant", WELCOME_TEXT)
        return WELCOME_TEXT

    history = get_recent_messages("whatsapp", user_id, limit=10)
    if settings.WHATSAPP_AI_ENABLED and settings.ANTHROPIC_API_KEY:
        reply = generate_whatsapp_reply(text, history)
    else:
        reply = WELCOME_TEXT

    upsert_state("whatsapp", user_id, "active", text)
    log_message("whatsapp", user_id, "assistant", reply)
    return reply
