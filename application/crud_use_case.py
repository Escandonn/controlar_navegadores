from infrastructure.data_repository import data_repository
from typing import List, Dict, Any


def get_all_records_use_case() -> List[Dict[str, Any]]:
    return data_repository.get_all_records()


def add_record_use_case(record: Dict[str, Any]) -> Dict[str, Any]:
    return data_repository.add_record(record)


def update_record_use_case(record_id: int, updated_record: Dict[str, Any]) -> bool:
    return data_repository.update_record(record_id, updated_record)


def delete_record_use_case(record_id: int) -> bool:
    return data_repository.delete_record(record_id)