import logging
import os

from core.config import WHATSAPP_URL
from core.profile import Profile
from infrastructure.bot_personality_service import get_personality_context
from seleniumbase import SB

logging.basicConfig(level=logging.INFO)


def open_profile_browser(profile: Profile):
    if profile.browser_slug != "chrome":
        raise NotImplementedError(f"Solo soporte Chrome por ahora, no '{profile.navegador}'.")

    user_data_dir = profile.user_data_dir
    if not os.path.exists(user_data_dir):
        raise FileNotFoundError(f"No existe el directorio de perfil: {user_data_dir}")

    personality_data = get_personality_context(profile)
    logging.info(
        "Abriendo bot '%s' con personalidad '%s' y contexto '%s' en %s",
        profile.nombre,
        personality_data["personalidad"],
        personality_data["contexto"],
        user_data_dir,
    )

    with SB(browser="chrome", headed=True, user_data_dir=user_data_dir) as sb:
        sb.open(WHATSAPP_URL)
        sb.wait_for_element("body", timeout=30)
        sb.execute_script(
            "console.log('Bot abierto con personalidad: %s - contexto: %s');"
            % (personality_data["personalidad"], personality_data["contexto"])
        )
        sb.sleep(999999)
