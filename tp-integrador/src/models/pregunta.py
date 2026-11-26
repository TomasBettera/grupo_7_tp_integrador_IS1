from datetime import datetime

from src.extensions import db

pregunta_tag = db.Table(
    "pregunta_tag",
    db.Column("pregunta_id", db.ForeignKey("preguntas.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tags.id"), primary_key=True),
)

class Pregunta(db.Model):
    __tablename__ = "preguntas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(
        db.DateTime, default=datetime.now, nullable=False
    )

    categoria_id = db.Column(db.ForeignKey("categorias.id"), nullable=False)
    autor_id = db.Column(db.ForeignKey("autores.id"), nullable=False)

    usuario_id = db.synonym("autor_id")

    categoria = db.relationship("Categoria", back_populates="preguntas")
    autor = db.relationship("Autor")
    tags = db.relationship(
        "Tag", secondary=pregunta_tag, back_populates="preguntas"
    )
    respuestas = db.relationship(
        "Respuesta", back_populates="pregunta", cascade="all, delete-orphan"
    )

    def agregar_respuesta(self, r):
        self.respuestas.append(r)

    def aceptar_respuesta(self, r):
        if r not in self.respuestas:
            raise ValueError("La respuesta no pertenece a esta pregunta")
        r.marcar_aceptada()

    def esta_sin_responder(self):
        return len(self.respuestas) == 0

    def tiempo_transcurrido(self):
        return datetime.now() - self.fecha_publicacion

    def supero_tiempo_limite(self, limite):
        return self.tiempo_transcurrido() > limite

    def tiene_etiqueta(self, nombre):
        return any(t.nombre == nombre for t in self.tags)

    def __repr__(self):
        return f"<Pregunta {self.id}: {self.titulo}>"