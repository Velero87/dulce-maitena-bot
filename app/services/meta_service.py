import os
import mimetypes
import requests
from app.config import settings



def _graph_url(path: str) -> str:
    return f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/{path}"



def send_whatsapp_text(to_number: str, body: str) -> dict:
    url = _graph_url(f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages")
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": body[:4096]},
    }
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return {
        "ok": response.ok,
        "status_code": response.status_code,
        "json": response.json() if response.content else {},
        "text": response.text,
    }



def send_whatsapp_template(to_number: str, template_name: str, lang_code: str = "es_AR") -> dict:
    url = _graph_url(f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages")
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": lang_code},
        },
    }
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return {
        "ok": response.ok,
        "status_code": response.status_code,
        "json": response.json() if response.content else {},
        "text": response.text,
    }



def publish_instagram_image(caption: str, image_url: str) -> dict:
    create_url = _graph_url(f"{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media")
    publish_url = _graph_url(f"{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish")
    headers = {"Authorization": f"Bearer {settings.META_ACCESS_TOKEN}"}

    create_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": settings.META_ACCESS_TOKEN,
    }
    create_resp = requests.post(create_url, data=create_payload, headers=headers, timeout=30)
    create_resp.raise_for_status()
    creation_id = create_resp.json()["id"]

    publish_payload = {
        "creation_id": creation_id,
        "access_token": settings.META_ACCESS_TOKEN,
    }
    publish_resp = requests.post(publish_url, data=publish_payload, headers=headers, timeout=30)
    publish_resp.raise_for_status()
    return publish_resp.json()



def local_image_to_public_url(local_path: str) -> str:
    filename = os.path.basename(local_path)
    return f"{settings.APP_BASE_URL}/static/{filename}"



def guess_mime_type(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "image/jpeg"
