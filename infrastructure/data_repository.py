from typing import List, Dict, Any


class DataRepository:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []
        self.next_id = 1

    def get_all_records(self) -> List[Dict[str, Any]]:
        return self.records.copy()

    def add_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        record['id'] = self.next_id
        self.next_id += 1
        self.records.append(record)
        return record

    def update_record(self, record_id: int, updated_record: Dict[str, Any]) -> bool:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                updated_record['id'] = record_id
                self.records[i] = updated_record
                return True
        return False

    def delete_record(self, record_id: int) -> bool:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                del self.records[i]
                return True
        return False

    def get_record_by_id(self, record_id: int) -> Dict[str, Any]:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                return rec
        return None


# Singleton instance
data_repository = DataRepository()