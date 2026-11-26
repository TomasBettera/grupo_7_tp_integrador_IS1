from flask import Blueprint, redirect, render_template, request, url_for
from src.extensions import db
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.estrategia.estrategia_local import EstrategiaLocal

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    preguntas = Pregunta.query.order_by(Pregunta.fecha_publicacion.desc()).all()
    return render_template("index.html", preguntas=preguntas)


@web_bp.route("/preguntas/nueva", methods=["GET", "POST"])
def nueva_pregunta():
    categorias = Categoria.query.all()
    if request.method == "POST":
        titulo = request.form["titulo"]
        cuerpo = request.form["cuerpo"]
        categoria_id = int(request.form["categoria_id"])
        usuario_id = 1  # Ajustar según el primer Autor/Usuario cargado en la BD

        pregunta = Pregunta(
            titulo=titulo,
            cuerpo=cuerpo,
            categoria_id=categoria_id,
            usuario_id=usuario_id,
        )
        db.session.add(pregunta)
        db.session.flush()  # Obtiene pregunta.id antes del commit

        # Genera respuesta automática usando la estrategia por defecto
        estrategia = EstrategiaLocal()
        texto_ia = estrategia.generar(f"{titulo}: {cuerpo}")
        respuesta_auto = Respuesta(
            cuerpo=texto_ia,
            pregunta_id=pregunta.id,
            autor_id=usuario_id,
        )
        db.session.add(respuesta_auto)
        db.session.commit()

        return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))

    return render_template("nueva_pregunta.html", categorias=categorias)


@web_bp.route("/preguntas/<int:pregunta_id>", methods=["GET", "POST"])
def detalle_pregunta(pregunta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    if request.method == "POST":
        cuerpo = request.form["cuerpo"]
        respuesta = Respuesta(
            cuerpo=cuerpo,
            pregunta_id=pregunta.id,
            autor_id=1,
        )
        db.session.add(respuesta)
        db.session.commit()
        return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))

    return render_template("detalle_pregunta.html", pregunta=pregunta)