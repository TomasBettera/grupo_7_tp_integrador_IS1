from src.fabricas.fabrica_autor import FabricaAutor
from src.models.autor import TUsuario
from src.models.usuario import Usuario


class FabricaUsuario(FabricaAutor):

    def crear_usuario(
        self,
        email: str,
        password: str,
        tipo: TUsuario = TUsuario.General,
    ) -> Usuario:
        return Usuario(email=email, password=password, tipo=tipo)

    def crearUsuario(
        self,
        email: str,
        password: str,
        tipo: TUsuario = TUsuario.General,
    ) -> Usuario:
        return self.crear_usuario(email=email, password=password, tipo=tipo)

    def crear_autor(
        self,
        email: str,
        password: str,
        tipo: TUsuario = TUsuario.General,
    ) -> Usuario:
        return self.crear_usuario(email=email, password=password, tipo=tipo)