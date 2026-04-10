from anthropic import Anthropic
from app.config import settings



def _get_client() -> Anthropic:
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)



def generate_instagram_post() -> str:
    client = _get_client()
    prompt = f"""
Sos especialista en marketing gastronómico argentino.
Marca: {settings.BUSINESS_NAME}
Producto: alfajores de maicena premium caseros.
Objetivo: vender por WhatsApp.
Ciudad foco: {settings.DEFAULT_CITY}.

Generá UN caption para Instagram en español rioplatense.
Reglas:
- 1 gancho inicial.
- 1 descripción apetecible.
- 1 CTA claro a WhatsApp.
- 5 hashtags relevantes.
- No uses comillas.
- Máximo 120 palabras.
"""
    response = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text_blocks = [b.text for b in response.content if hasattr(b, "text")]
    return "\n".join(text_blocks).strip()



def generate_whatsapp_reply(user_text: str, history: list[dict]) -> str:
    client = _get_client()

    price_lines = []
    if settings.ORDER_PRICE_6:
        price_lines.append(f"- 6 alfajores: {settings.ORDER_PRICE_6}")
    if settings.ORDER_PRICE_12:
        price_lines.append(f"- 12 alfajores: {settings.ORDER_PRICE_12}")
    prices_text = "\n".join(price_lines) if price_lines else "- No hay precios cargados todavía"

    system_prompt = f"""
Sos el asistente de ventas por WhatsApp de {settings.BUSINESS_NAME}, una marca argentina de alfajores de maicena.

Datos del negocio:
- Ciudad base: {settings.DEFAULT_CITY}
- Catálogo/wa link: {settings.ORDER_CATALOG_URL}
- Medios de pago: {settings.ORDER_PAYMENT_METHODS}
- Precios cargados:
{prices_text}

Tu objetivo:
- responder cálido, breve y útil
- guiar al cliente para cerrar venta
- pedir datos concretos: cantidad, zona, si retira o si quiere envío
- no inventar precios, stock ni tiempos si no están cargados
- si el tema es pago, comprobante, transferencia, urgencia o reclamo, indicá que sigue un humano

Reglas:
- escribí en español de Argentina
- máximo 5 líneas
- no digas que sos IA
- no uses markdown
- si saludan, saludá y guiá
- si preguntan precio y hay precios cargados, usalos
- si preguntan envío, pedí barrio o zona
- si preguntan por mayorista, eventos o pedidos especiales, derivá a humano
""".strip()

    messages = []
    for item in history[-8:]:
        role = item.get("role", "user")
        content = item.get("content", "")
        if not content:
            continue
        messages.append({"role": "assistant" if role == "assistant" else "user", "content": content})

    if not history or history[-1].get("content") != user_text:
        messages.append({"role": "user", "content": user_text})

    response = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=220,
        system=system_prompt,
        messages=messages,
    )
    text_blocks = [b.text for b in response.content if hasattr(b, "text")]
    return "\n".join(text_blocks).strip()
