from abc import abstractmethod
from enum import Enum
from uuid import uuid4
from src.extensions import db

class TUsuario(str, Enum):
    ADMIN = "Admin"
    GENERAL = "General"
    Admin = "Admin"
    General = "General"

class Autor(db.Model):
    __tablename__ = "autores"

    id = db.Column(db.String(50), primary_key=True, default=lambda: uuid4().hex)
    tipo_autor = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "autor",
        "polymorphic_on": tipo_autor,
    }

    def obtener_id(self) -> str:
        return self.id

    def obtenerId(self) -> str:
        return self.id

    @property
    def tipo(self) -> str:
        return self.tipo_autor

    @abstractmethod
    def obtener_nombre(self) -> str:
        raise NotImplementedError

    def obtenerNombre(self) -> str:
        return self.obtener_nombre()
