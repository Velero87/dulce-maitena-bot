# Dulce Maitena - automatización Instagram + WhatsApp

Proyecto listo para copiar/pegar y poner en marcha con Python.

## Qué hace ahora
- Genera contenido con Claude.
- Publica automáticamente en Instagram si tenés listo el ID de Instagram y el token.
- Recibe mensajes de WhatsApp por webhook.
- Responde automáticamente con IA a consultas de WhatsApp.
- Guarda un historial simple de mensajes en SQLite.
- Deriva a humano cuando detecta palabras sensibles como pago, comprobante o urgente.

## Qué no hace por sí solo
- No fabrica fotos. Usa una foto real tuya en `content/images/`.
- No cobra pagos.
- No reemplaza aprobaciones obligatorias de Meta.

## Estructura importante
- `app.py`: arranque del proyecto.
- `app/config.py`: variables de entorno.
- `app/main.py`: endpoints y webhook.
- `app/services/claude_service.py`: genera caption y respuestas IA.
- `app/services/meta_service.py`: envía mensajes a WhatsApp y publica en Instagram.
- `app/services/whatsapp_bot.py`: lógica del bot.
- `app/db.py`: base local SQLite.

## Instalación local
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Ejecutar
```bash
python app.py
```

## Endpoints útiles
- `GET /health`
- `GET /meta/webhook` -> verificación del webhook de Meta
- `POST /meta/webhook` -> recibe mensajes de WhatsApp
- `POST /manual/publish` -> fuerza una publicación de Instagram

## Flujo de WhatsApp IA
1. El cliente manda un mensaje a tu número.
2. Meta lo manda a tu webhook.
3. Tu proyecto guarda el mensaje en SQLite.
4. Claude arma una respuesta breve para vender.
5. Tu proyecto responde por WhatsApp.
6. Si la conversación está fuera de la ventana permitida y cargaste un template, intenta usarlo.

## Despliegue simple en Render
1. Subí esta carpeta a GitHub.
2. Creá un `Web Service` en Render.
3. Runtime: Python.
4. Start command: `python app.py`.
5. Cargá todas las variables del `.env` en Render.
6. En Meta, poné el webhook: `https://TU-APP.onrender.com/meta/webhook`

## Antes de probar de verdad
- Cargá precios en `.env`.
- Probá primero con tu propio número.
- No pegues tokens reales en chats o capturas compartidas.
