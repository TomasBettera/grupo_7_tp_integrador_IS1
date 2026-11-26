from src.fabricas.fabrica_autor import FabricaAutor
from src.models.autor import TUsuario
from src.models.usuario import Usuario


class FabricaUsuario(FabricaAutor):
    def __init__(self, email: str, password: str, tipo: TUsuario = TUsuario.GENERAL):
        self.email = email
        self.password = password
        self.tipo = tipo

    def crear_autor(self, **kwargs) -> Usuario:
        email = kwargs.get("email", self.email)
        password = kwargs.get("password", self.password)
        tipo = kwargs.get("tipo", self.tipo)
        return Usuario(email=email, password=password, tipo=tipo)

    def crearAutor(self, **kwargs) -> Usuario:
        return self.crear_autor(**kwargs)
