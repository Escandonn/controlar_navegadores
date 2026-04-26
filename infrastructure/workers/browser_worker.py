import multiprocessing
from typing import List

from infrastructure.selenium.selenium_service import open_profile_browser
from core.profile import Profile


def run_profile_browsers(profiles: List[Profile]) -> None:
    """Ejecuta un proceso por cada perfil activo o seleccionado."""
    processes = []
    for profile in profiles:
        process = multiprocessing.Process(target=open_profile_browser, args=(profile,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
