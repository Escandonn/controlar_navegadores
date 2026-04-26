from dataclasses import dataclass, field
from typing import List
import os


@dataclass
class Profile:
    id: int
    nombre: str
    navegador: str
    email: str = ""
    contrasena: str = ""
    aplicaciones: List[str] = field(default_factory=list)
    fecha: str = ""
    estado: str = "Activo"
    notas: str = ""
    personalidad: str = ""
    contexto: str = ""

    @property
    def esta_activo(self) -> bool:
        return self.estado.strip().lower() == "activo"

    @property
    def browser_slug(self) -> str:
        return self.navegador.strip().lower()

    @property
    def user_data_dir(self) -> str:
        base_name = self.browser_slug
        if base_name == "chrome":
            return os.path.abspath(os.path.join("profiles", "chrome", self.nombre))
        return os.path.abspath(os.path.join("profiles", base_name, self.nombre))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "navegador": self.navegador,
            "email": self.email,
            "contrasena": self.contrasena,
            "aplicaciones": self.aplicaciones,
            "fecha": self.fecha,
            "estado": self.estado,
            "notas": self.notas,
            "personalidad": self.personalidad,
            "contexto": self.contexto,
        }
