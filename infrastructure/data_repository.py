from dataclasses import asdict
from typing import List, Dict, Any
import json
import os

from core.profile import Profile


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
            pass

    def _to_profile(self, record: Dict[str, Any]) -> Profile:
        return Profile(
            id=record.get('id', 0),
            nombre=record.get('nombre', ''),
            navegador=record.get('navegador', 'Chrome'),
            email=record.get('email', ''),
            contrasena=record.get('contrasena', ''),
            aplicaciones=record.get('aplicaciones', []),
            fecha=record.get('fecha', ''),
            estado=record.get('estado', 'Activo'),
            notas=record.get('notas', ''),
            personalidad=record.get('personalidad', ''),
            contexto=record.get('contexto', ''),
        )

    def _normalize_record(self, record: Any) -> Dict[str, Any]:
        if isinstance(record, Profile):
            record = asdict(record)
        if 'aplicaciones' not in record or record['aplicaciones'] is None:
            record['aplicaciones'] = []
        if 'personalidad' not in record:
            record['personalidad'] = ''
        if 'contexto' not in record:
            record['contexto'] = ''
        return record

    def get_all_records(self) -> List[Profile]:
        return [self._to_profile(rec) for rec in self.records]

    def get_active_records(self) -> List[Profile]:
        return [profile for profile in self.get_all_records() if profile.esta_activo]

    def get_records_by_ids(self, record_ids: List[int]) -> List[Profile]:
        return [profile for profile in self.get_all_records() if profile.id in record_ids]

    def add_record(self, record: Any) -> Profile:
        normalized = self._normalize_record(record)
        normalized['id'] = self.next_id
        self.next_id += 1
        self.records.append(normalized)
        self.save_data()
        return self._to_profile(normalized)

    def update_record(self, record_id: int, updated_record: Any) -> bool:
        normalized = self._normalize_record(updated_record)
        for i, rec in enumerate(self.records):
            if rec['id'] == record_id:
                normalized['id'] = record_id
                self.records[i] = normalized
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

    def get_record_by_id(self, record_id: int) -> Profile:
        for rec in self.records:
            if rec['id'] == record_id:
                return self._to_profile(rec)
        return None


# Instancia singleton
data_repository = DataRepository()