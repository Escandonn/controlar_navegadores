from application.browser_use_case import (
    run_active_profiles_use_case,
    run_selected_profiles_use_case
)
from application.crud_use_case import (
    get_all_profiles_use_case,
    get_active_profiles_use_case,
    get_profiles_by_ids_use_case,
    add_record_use_case,
    update_record_use_case,
    delete_record_use_case
)
from typing import List
from core.profile import Profile


class AppController:

    def open_active_profiles(self) -> None:
        run_active_profiles_use_case()

    def open_selected_profiles(self, profile_ids: List[int]) -> None:
        run_selected_profiles_use_case(profile_ids)

    def get_all_profiles(self) -> List[Profile]:
        return get_all_profiles_use_case()

    def get_active_profiles(self) -> List[Profile]:
        return get_active_profiles_use_case()

    def get_profiles_by_ids(self, profile_ids: List[int]) -> List[Profile]:
        return get_profiles_by_ids_use_case(profile_ids)

    def add_record(self, record: Profile) -> Profile:
        return add_record_use_case(record)

    def update_record(self, record_id: int, updated_record: Profile) -> bool:
        return update_record_use_case(record_id, updated_record)

    def delete_record(self, record_id: int) -> bool:
        return delete_record_use_case(record_id)