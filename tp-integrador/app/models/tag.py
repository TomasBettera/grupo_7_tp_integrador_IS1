from app.extensions import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))

    preguntas = db.relationship(
        "Pregunta", secondary="pregunta_tag", back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.nombre}>"