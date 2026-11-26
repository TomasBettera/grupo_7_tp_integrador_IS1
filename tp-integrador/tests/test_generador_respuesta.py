from datetime import datetime, timedelta

from src.estrategia.estrategia_gemini import EstrategiaGemini
from src.estrategia.estrategia_local import EstrategiaLocal
from src.estrategia.estrategia_openai import EstrategiaOpenAI
from src.models.agente_ia import AgenteIA
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta
from src.models.tag import Tag
from src.services.generador_respuesta import GeneradorRespuestaAutomatica


def test_debe_activarse_con_etiqueta_ia(session):
    cat = Categoria(nombre="Programación")
    tag_ia = Tag(nombre="ia-help")
    autor = AgenteIA(nombre="UserTest")
    session.add_all([cat, tag_ia, autor])
    session.commit()

    p = Pregunta(titulo="Ayuda en Python", cuerpo="¿Cómo funciona GIL?", categoria=cat, autor=autor)
    p.tags.append(tag_ia)
    session.add(p)
    session.commit()

    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaGemini())
    assert generador.debe_activarse(p) is True
    assert generador.debeActivarse(p) is True


def test_debe_activarse_por_tiempo_inactiva(session):
    cat = Categoria(nombre="Bases de Datos")
    autor = AgenteIA(nombre="UserTest2")
    session.add_all([cat, autor])
    session.commit()

    hace_dos_dias = datetime.now() - timedelta(hours=48)
    p = Pregunta(titulo="Duda SQL", cuerpo="Explicar JOIN", categoria=cat, autor=autor, fecha_publicacion=hace_dos_dias)
    session.add(p)
    session.commit()

    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaLocal(), umbral_tiempo_espera=timedelta(hours=24))
    assert generador.debe_activarse(p) is True


def test_no_debe_activarse_si_no_supero_tiempo_y_no_tiene_tag(session):
    cat = Categoria(nombre="Redes")
    autor = AgenteIA(nombre="UserTest3")
    session.add_all([cat, autor])
    session.commit()

    p = Pregunta(titulo="Duda TCP", cuerpo="Explicar Handshake", categoria=cat, autor=autor)
    session.add(p)
    session.commit()

    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaOpenAI(), umbral_tiempo_espera=timedelta(hours=24))
    assert generador.debe_activarse(p) is False


def test_generar_para_con_diferentes_estrategias(session):
    cat = Categoria(nombre="Software")
    autor_preg = AgenteIA(nombre="Estudiante")
    agente_bot = AgenteIA(nombre="Asistente Bot")
    session.add_all([cat, autor_preg, agente_bot])
    session.commit()

    p = Pregunta(titulo="¿Qué es Strategy?", cuerpo="Explique el patrón", categoria=cat, autor=autor_preg)
    session.add(p)
    session.commit()

    generador_openai = GeneradorRespuestaAutomatica(estrategia=EstrategiaOpenAI(), agente=agente_bot)
    r1 = generador_openai.generar_para(p)
    session.add(r1)
    session.commit()

    assert r1.id is not None
    assert "OpenAI" in r1.cuerpo
    assert r1.pregunta_id == p.id
    assert r1.autor_id == agente_bot.id
    assert r1 in p.respuestas

    generador_gemini = GeneradorRespuestaAutomatica(estrategia=EstrategiaGemini(), agente=agente_bot)
    r2 = generador_gemini.generar_para(p)
    session.add(r2)
    session.commit()

    assert "Gemini" in r2.cuerpo
    assert len(p.respuestas) == 2