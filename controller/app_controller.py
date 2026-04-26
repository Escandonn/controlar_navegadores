from application.browser_use_case import run_browsers_use_case
from application.crud_use_case import (
    get_all_records_use_case,
    add_record_use_case,
    update_record_use_case,
    delete_record_use_case
)
from typing import List, Dict, Any


class AppController:

    def start_browsers(self):
        run_browsers_use_case()

    def get_all_records(self) -> List[Dict[str, Any]]:
        return get_all_records_use_case()

    def add_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return add_record_use_case(record)

    def update_record(self, record_id: int, updated_record: Dict[str, Any]) -> bool:
        return update_record_use_case(record_id, updated_record)

    def delete_record(self, record_id: int) -> bool:
        return delete_record_use_case(record_id)