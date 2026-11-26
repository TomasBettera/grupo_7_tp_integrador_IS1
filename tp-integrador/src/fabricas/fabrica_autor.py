from abc import ABC, abstractmethod
from src.models.autor import Autor

class FabricaAutor(ABC):
    @abstractmethod
    def crear_autor(self, **kwargs) -> Autor:
        pass

    def crearAutor(self, **kwargs) -> Autor:
        return self.crear_autor(**kwargs)
