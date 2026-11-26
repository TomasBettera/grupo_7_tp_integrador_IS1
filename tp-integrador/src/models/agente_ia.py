from src.extensions import db
from src.models.autor import Autor


class AgenteIA(Autor):
    __tablename__ = "agentes_ia"

    id = db.Column(db.String(50), db.ForeignKey("autores.id"), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, default="Agente IA")
    activo = db.Column(db.Boolean, default=True, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "agente_ia",
    }

    def __init__(self, nombre: str = "Agente IA", activo: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.activo = activo

    def obtener_nombre(self) -> str:
        return self.nombre

    def obtenerNombre(self) -> str:
        return self.obtener_nombre()

    def esta_activo(self) -> bool:
        return self.activo

    def __repr__(self) -> str:
        return f"<AgenteIA {self.id}: {self.nombre} (Activo={self.activo})>"
