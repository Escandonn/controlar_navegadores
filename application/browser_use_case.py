from infrastructure.workers.browser_worker import run_profile_browsers
from infrastructure.data_repository import data_repository
from typing import List, Optional
from core.profile import Profile


def run_active_profiles_use_case() -> None:
    """Inicia todos los perfiles activos."""
    profiles = data_repository.get_active_records()
    run_profile_browsers(profiles)


def run_selected_profiles_use_case(profile_ids: List[int]) -> None:
    """Inicia los perfiles seleccionados por ID."""
    profiles = data_repository.get_records_by_ids(profile_ids)
    run_profile_browsers(profiles)

