from infrastructure.data_repository import data_repository
from typing import List
from core.profile import Profile


def get_all_profiles_use_case() -> List[Profile]:
    return data_repository.get_all_records()


def get_active_profiles_use_case() -> List[Profile]:
    return data_repository.get_active_records()


def get_profiles_by_ids_use_case(profile_ids: List[int]) -> List[Profile]:
    return data_repository.get_records_by_ids(profile_ids)


def add_record_use_case(record: Profile) -> Profile:
    return data_repository.add_record(record)


def update_record_use_case(record_id: int, updated_record: Profile) -> bool:
    return data_repository.update_record(record_id, updated_record)


def delete_record_use_case(record_id: int) -> bool:
    return data_repository.delete_record(record_id)