import os
from flask import Flask, jsonify, request, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.db import init_db
from app.services.claude_service import generate_instagram_post
from app.services.meta_service import (
    publish_instagram_image,
    send_whatsapp_text,
    send_whatsapp_template,
    local_image_to_public_url,
)
from app.services.whatsapp_bot import handle_whatsapp_message, NON_TEXT_TEXT



def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    init_db()

    scheduler = BackgroundScheduler(timezone=settings.TIMEZONE)
    scheduler.add_job(
        func=lambda: safe_daily_publish(app),
        trigger="cron",
        hour=settings.AUTO_POST_HOUR,
        minute=settings.AUTO_POST_MINUTE,
        id="daily_instagram_post",
        replace_existing=True,
    )
    scheduler.start()

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "business": settings.BUSINESS_NAME, "whatsapp_ai": settings.WHATSAPP_AI_ENABLED})

    @app.get("/static/<path:filename>")
    def static_files(filename: str):
        directory = os.path.abspath("content/images")
        return send_from_directory(directory, filename)

    @app.get("/meta/webhook")
    def verify_webhook():
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            return challenge, 200
        return "forbidden", 403

        @app.post("/meta/webhook")
    def receive_webhook():
        payload = request.get_json(silent=True) or {}
        print("[WEBHOOK_RAW]", payload, flush=True)

        try:
            for entry in payload.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    print("[WEBHOOK_VALUE]", value, flush=True)

                    messages = value.get("messages", [])
                    contacts = value.get("contacts", [])

                    if not messages:
                        print("[WEBHOOK_NO_MESSAGES]", flush=True)
                        continue

                    incoming = messages[0]
                    sender = incoming.get("from")
                    msg_type = incoming.get("type")
                    text = incoming.get("text", {}).get("body", "").strip()

                    print("[WEBHOOK_SENDER]", sender, flush=True)
                    print("[WEBHOOK_TYPE]", msg_type, flush=True)
                    print("[WEBHOOK_TEXT]", text, flush=True)

                    if not sender:
                        print("[WEBHOOK_NO_SENDER]", flush=True)
                        continue

                    if msg_type != "text":
                        print("[WEBHOOK_NON_TEXT_REPLY]", NON_TEXT_TEXT, flush=True)
                        result = send_whatsapp_text(sender, NON_TEXT_TEXT)
                        print("[WHATSAPP_SEND_RESULT]", result, flush=True)
                        maybe_resume_template(result, sender)
                        continue

                    reply = handle_whatsapp_message(sender, text)
                    print("[BOT_REPLY]", reply, flush=True)

                    result = send_whatsapp_text(sender, reply)
                    print("[WHATSAPP_SEND_RESULT]", result, flush=True)

                    maybe_resume_template(result, sender)

            return jsonify({"received": True})
        except Exception as exc:
            print("[WEBHOOK_ERROR]", str(exc), flush=True)
            return jsonify({"error": str(exc)}), 500

    @app.post("/manual/publish")
    def manual_publish():
        result = do_publish()
        return jsonify(result)

    return app



def maybe_resume_template(send_result: dict, sender: str) -> None:
    if send_result.get("ok"):
        return

    error_text = (send_result.get("text") or "").lower()
    if settings.WHATSAPP_TEMPLATE_RESUME and ("24" in error_text or "outside the allowed window" in error_text or "131047" in error_text):
        send_whatsapp_template(sender, settings.WHATSAPP_TEMPLATE_RESUME)



def do_publish() -> dict:
    caption = generate_instagram_post()
    image_public_url = local_image_to_public_url(settings.DEFAULT_IMAGE_PATH)
    publish_result = publish_instagram_image(caption=caption, image_url=image_public_url)
    return {
        "success": True,
        "caption": caption,
        "publish_result": publish_result,
    }



def safe_daily_publish(app: Flask) -> None:
    with app.app_context():
        try:
            result = do_publish()
            print("[AUTO_PUBLISH_OK]", result)
        except Exception as exc:
            print("[AUTO_PUBLISH_ERROR]", str(exc))
