import json
import urllib.request
import urllib.error
from typing import Dict

from core.config import PERSONALITY_API_URL
from core.profile import Profile


def get_personality_context(profile: Profile) -> Dict[str, str]:
    """Obtiene la personalidad y el contexto de la API externa.
    Si la API no está disponible, regresa valores por defecto basados en el perfil.
    """
    payload = json.dumps({
        "nombre": profile.nombre,
        "personalidad": profile.personalidad,
        "contexto": profile.contexto,
        "navegador": profile.navegador,
    }).encode("utf-8")

    request = urllib.request.Request(
        PERSONALITY_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)
            return {
                "personalidad": result.get("personalidad", profile.personalidad or "Bot de WhatsApp"),
                "contexto": result.get("contexto", profile.contexto or "Automatización de WhatsApp Web"),
            }
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return {
            "personalidad": profile.personalidad or "Bot de WhatsApp",
            "contexto": profile.contexto or "Automatización de WhatsApp Web",
        }
