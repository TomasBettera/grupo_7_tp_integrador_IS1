from src.fabricas.fabrica_autor import FabricaAutor
from src.models.agente_ia import AgenteIA


class FabricaAgenteIA(FabricaAutor):

    def crear_autor(self, nombre: str = "Agente IA", activo: bool = True, **kwargs) -> AgenteIA:
        return AgenteIA(nombre=nombre, activo=activo, **kwargs)

    def crearAutor(self, nombre: str = "Agente IA", activo: bool = True, **kwargs) -> AgenteIA:
        return self.crear_autor(nombre=nombre, activo=activo, **kwargs)
