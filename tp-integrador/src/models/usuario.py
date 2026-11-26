from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions import db
from src.models.autor import Autor, TUsuario


class Usuario(Autor):
    __tablename__ = "usuarios"

    id = db.Column(
        db.String, db.ForeignKey("autores.id"), primary_key=True
    )
    email = db.Column(db.String(255), nullable=False, unique=True)
    passwordHash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum(TUsuario, name="tipo_usuario"), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "usuario"}

    def __init__(self, email: str, password: str, tipo: TUsuario):
        if not isinstance(email, str) or not email.strip():
            raise ValueError("El email es obligatorio")
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña es obligatoria")
        if not isinstance(tipo, TUsuario):
            raise ValueError("El rol debe ser un valor de TUsuario")

        super().__init__(
            id=uuid4().hex,
            email=email.strip().lower(),
            passwordHash=generate_password_hash(password),
            tipo=tipo,
        )

    def registrarse(self) -> None:
        db.session.add(self)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def autenticar(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        return check_password_hash(self.passwordHash, password)

    def obtenerNombre(self) -> str:
        return self.email