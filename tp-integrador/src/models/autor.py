from abc import ABC, ABCMeta, abstractmethod
from enum import Enum

from src.extensions import db


class TUsuario(Enum):
    Admin = "Admin"
    General = "General"


class _ABCModelMeta(type(db.Model), ABCMeta):
    pass


class Autor(db.Model, ABC, metaclass=_ABCModelMeta):
    __tablename__ = "autores"

    id = db.Column(db.String, primary_key=True)
    tipo_autor = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": tipo_autor,
        "polymorphic_identity": "autor",
    }

    @abstractmethod
    def obtenerNombre(self) -> str:
        raise NotImplementedError

    def obtenerId(self) -> str:
        return self.id