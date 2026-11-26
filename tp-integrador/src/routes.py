import inspect
from flask import Blueprint, redirect, render_template, request, url_for
from src.extensions import db
from src.models.agente_ia import AgenteIA
from src.models.autor import Autor
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.estrategia.estrategia_local import EstrategiaLocal
from src.estrategia.estrategia_gemini import EstrategiaGemini
from src.estrategia.estrategia_openai import EstrategiaOpenAI
from src.services.generador_respuesta import GeneradorRespuestaAutomatica

web_bp = Blueprint("web", __name__)

ESTRATEGIAS = {
    "local": EstrategiaLocal,
    "gemini": EstrategiaGemini,
    "openai": EstrategiaOpenAI,
}


def _instanciar_estrategia(estrategia_key: str, modelo: str):
    clase_estrategia = ESTRATEGIAS.get(estrategia_key, EstrategiaLocal)
    modelo = (modelo or "").strip()
    if not modelo:
        return clase_estrategia()

    params = inspect.signature(clase_estrategia.__init__).parameters
    if "modelo" in params:
        return clase_estrategia(modelo=modelo)
    if "model" in params:
        return clase_estrategia(model=modelo)

    instancia = clase_estrategia()
    if hasattr(instancia, "modelo"):
        instancia.modelo = modelo
    elif hasattr(instancia, "model"):
        instancia.model = modelo
    return instancia


def _generar_respuesta_ia(pregunta: Pregunta, estrategia_key: str, modelo: str = ""):
    agente_existente = AgenteIA.query.filter_by(nombre="Bot Asistente IA").first()
    estrategia = _instanciar_estrategia(estrategia_key, modelo)
    generador = GeneradorRespuestaAutomatica(
        estrategia=estrategia,
        agente=agente_existente,
    )
    respuesta_auto = generador.generar_para(pregunta)
    db.session.add(respuesta_auto)


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
        estrategia_key = request.form.get("estrategia", "local")
        modelo = request.form.get("modelo", "")

        autor = Autor.query.first()
        usuario_id = autor.id if autor else 1

        pregunta = Pregunta(
            titulo=titulo,
            cuerpo=cuerpo,
            categoria_id=categoria_id,
            usuario_id=usuario_id,
        )
        db.session.add(pregunta)
        db.session.flush()

        _generar_respuesta_ia(pregunta, estrategia_key, modelo)
        db.session.commit()

        return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))

    return render_template("nueva_pregunta.html", categorias=categorias)


@web_bp.route("/preguntas/<int:pregunta_id>", methods=["GET", "POST"])
def detalle_pregunta(pregunta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    if request.method == "POST":
        cuerpo = request.form["cuerpo"]
        autor = Autor.query.first()
        respuesta = Respuesta(
            cuerpo=cuerpo,
            pregunta_id=pregunta.id,
            autor_id=autor.id if autor else 1,
        )
        db.session.add(respuesta)
        db.session.commit()
        return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))

    return render_template("detalle_pregunta.html", pregunta=pregunta)


@web_bp.route("/preguntas/<int:pregunta_id>/generar-ia", methods=["POST"])
def generar_ia_en_pregunta(pregunta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    estrategia_key = request.form.get("estrategia", "local")
    modelo = request.form.get("modelo", "")
    _generar_respuesta_ia(pregunta, estrategia_key, modelo)
    db.session.commit()
    return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))


@web_bp.route("/preguntas/<int:pregunta_id>/aceptar/<int:respuesta_id>", methods=["POST"])
def aceptar_respuesta(pregunta_id, respuesta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    respuesta = Respuesta.query.get_or_404(respuesta_id)
    pregunta.aceptar_respuesta(respuesta)
    db.session.commit()
    return redirect(url_for("web.detalle_pregunta", pregunta_id=pregunta.id))