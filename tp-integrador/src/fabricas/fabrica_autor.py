from abc import ABC, abstractmethod

from src.models.autor import Autor


class FabricaAutor(ABC):

    @abstractmethod
    def crear_autor(self, *args, **kwargs) -> Autor:
        raise NotImplementedError

    def crearAutor(self, *args, **kwargs) -> Autor:
        return self.crear_autor(*args, **kwargs)
