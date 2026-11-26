from datetime import datetime

from src.extensions import db


class Respuesta(db.Model):
    __tablename__ = "respuestas"

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(
        db.DateTime, default=datetime.now, nullable=False
    )
    aceptada = db.Column(db.Boolean, default=False, nullable=False)

    pregunta_id = db.Column(db.ForeignKey("preguntas.id"), nullable=False)
    autor_id = db.Column(db.ForeignKey("autores.id"), nullable=False)

    pregunta = db.relationship("Pregunta", back_populates="respuestas")
    autor = db.relationship("Autor")

    def marcar_aceptada(self):
        self.aceptada = True

    def __repr__(self):
        return f"<Respuesta {self.id} de pregunta {self.pregunta_id}>"