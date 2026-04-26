from typing import List, Dict, Any
import json
import os


class DataRepository:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.records: List[Dict[str, Any]] = []
        self.next_id = 1
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = data.get('records', [])
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, IOError):
                # Si hay error, empezar vacío
                self.records = []
                self.next_id = 1

    def save_data(self):
        data = {
            'records': self.records,
            'next_id': self.next_id
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            # Si no puede guardar, continuar
            pass

    def get_all_records(self) -> List[Dict[str, Any]]:
        return self.records.copy()

    def add_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        record['id'] = self.next_id
        self.next_id += 1
        # Ensure aplicaciones is a list
        if 'aplicaciones' not in record:
            record['aplicaciones'] = []
        self.records.append(record)
        self.save_data()
        return record

    def update_record(self, record_id: int, updated_record: Dict[str, Any]) -> bool:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                updated_record['id'] = record_id
                self.records[i] = updated_record
                self.save_data()
                return True
        return False

    def delete_record(self, record_id: int) -> bool:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                del self.records[i]
                self.save_data()
                return True
        return False

    def get_record_by_id(self, record_id: int) -> Dict[str, Any]:
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                return rec
        return None


# Instancia singleton
data_repository = DataRepository()