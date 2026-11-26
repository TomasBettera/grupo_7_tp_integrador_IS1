from datetime import timedelta
import pytest
from sqlalchemy.exc import IntegrityError

from src.estrategia.estrategia_local import EstrategiaLocal
from src.estrategia.estrategia_openai import EstrategiaOpenAI
from src.estrategia.estrategia_gemini import EstrategiaGemini
from src.models.agente_ia import AgenteIA
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.models.tag import Tag
from src.models.usuario import Usuario
from src.models.autor import Autor, TUsuario
from src.services.generador_respuesta import GeneradorRespuestaAutomatica
from src.services.monitor_preguntas import MonitorPreguntasInactivas


def test_pregunta_aceptar_respuesta_valida_e_invalida(session):
    cat = Categoria(nombre="Matemática")
    autor = AgenteIA(nombre="Profesor")
    session.add_all([cat, autor])
    session.commit()

    p1 = Pregunta(titulo="P1", cuerpo="C1", categoria=cat, autor=autor)
    p2 = Pregunta(titulo="P2", cuerpo="C2", categoria=cat, autor=autor)
    r1 = Respuesta(cuerpo="R1 de P1", pregunta=p1, autor=autor)
    r2 = Respuesta(cuerpo="R2 de P2", pregunta=p2, autor=autor)
    p1.agregar_respuesta(r1)
    p2.agregar_respuesta(r2)
    session.add_all([p1, p2, r1, r2])
    session.commit()

    # Caso válido: aceptar respuesta perteneciente a p1
    assert r1.aceptada is False
    p1.aceptar_respuesta(r1)
    assert r1.aceptada is True

    # Caso inválido: intentar aceptar en p1 una respuesta que pertenece a p2
    with pytest.raises(ValueError, match="La respuesta no pertenece a esta pregunta"):
        p1.aceptar_respuesta(r2)


def test_pregunta_invariantes_y_repr(session):
    cat = Categoria(nombre="Lógica")
    autor = AgenteIA(nombre="Bot")
    tag = Tag(nombre="logica-proposicional")
    p = Pregunta(titulo="Modus Ponens", cuerpo="Explicar regla", categoria=cat, autor=autor)
    p.tags.append(tag)
    session.add_all([cat, autor, tag, p])
    session.commit()

    assert p.tiene_etiqueta("logica-proposicional") is True
    assert p.tiene_etiqueta("etiqueta-inexistente") is False
    assert f"<Pregunta {p.id}: Modus Ponens>" == repr(p)


def test_respuesta_invariantes_y_repr(session):
    cat = Categoria(nombre="Algoritmos")
    autor = AgenteIA(nombre="Bot")
    p = Pregunta(titulo="QuickSort", cuerpo="Complejidad promedio", categoria=cat, autor=autor)
    r = Respuesta(cuerpo="O(n log n)", pregunta=p, autor=autor)
    session.add_all([cat, autor, p, r])
    session.commit()

    assert r.aceptada is False
    r.marcar_aceptada()
    assert r.aceptada is True
    assert f"<Respuesta {r.id} de pregunta {p.id}>" == repr(r)


def test_categoria_y_tag_repr(session):
    cat = Categoria(nombre="Estructuras Discretas")
    tag = Tag(nombre="grafos", descripcion="Teoría de grafos")
    session.add_all([cat, tag])
    session.commit()

    assert "<Categoria Estructuras Discretas>" == repr(cat)
    assert "<Tag grafos>" == repr(tag)


def test_agente_ia_repr_y_metodos():
    bot = AgenteIA(nombre="TuringBot", activo=True)
    assert "<AgenteIA None: TuringBot (Activo=True)>" == repr(bot)
    assert bot.esta_activo() is True


def test_usuario_registrarse_exitoso_y_duplicado(session):
    u1 = Usuario(email="usuario1@unrc.edu.ar", password="passwordSegura1", tipo=TUsuario.GENERAL)
    u1.registrarse()
    assert u1.id is not None

    # Intentar registrar otro usuario con el mismo email debe disparar IntegrityError
    u_duplicado = Usuario(email="usuario1@unrc.edu.ar", password="otraPassword", tipo=TUsuario.ADMIN)
    with pytest.raises(IntegrityError):
        u_duplicado.registrarse()


def test_estrategia_local_directa():
    est = EstrategiaLocal()
    res = est.generar("Prompt de prueba")
    assert "Respuesta generada para: Prompt de prueba" in res


def test_estrategias_gemini_y_openai():
    g = EstrategiaGemini()
    res_g = g.generar("Hola Gemini")
    assert "Gemini" in res_g

    o = EstrategiaOpenAI()
    res_o = o.generar("Hola OpenAI")
    assert "OpenAI" in res_o


def test_monitor_ejecucion_desde_db(session):
    cat = Categoria(nombre="General")
    autor = AgenteIA(nombre="AutoBot")
    tag_ia = Tag(nombre="ia-help")
    session.add_all([cat, autor, tag_ia])
    session.commit()

    p = Pregunta(titulo="Pregunta IA", cuerpo="Detalle", categoria=cat, autor=autor)
    p.tags.append(tag_ia)
    session.add(p)
    session.commit()

    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaLocal(), agente=autor)
    monitor = MonitorPreguntasInactivas(generador=generador)

    # Ejecuta sin pasar lista explícita (consulta Pregunta.query.all() de la BD)
    respuestas = monitor.ejecutarRevision(auto_commit=True)
    assert len(respuestas) == 1
    assert respuestas[0].pregunta_id == p.id


def test_metodos_base_autor_y_servicios(session):
    cat = Categoria(nombre="Matemática")
    autor = AgenteIA(nombre="Profesor Base")
    session.add_all([cat, autor])
    session.commit()

    # Métodos de Autor
    assert autor.obtener_id() == autor.id
    assert autor.obtenerId() == autor.id

    # Métodos y alias en GeneradorRespuestaAutomatica
    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaLocal(), agente=autor)
    tag_ia = Tag(nombre="ia-help")
    p = Pregunta(titulo="Lógica", cuerpo="Tautología", categoria=cat, autor=autor)
    p.tags.append(tag_ia)
    session.add_all([tag_ia, p])
    session.commit()

    assert generador.debeActivarse(p) is True
    r = generador.generarPara(p)
    assert r.pregunta == p
    session.add(r)
    session.commit()
    assert r.pregunta_id == p.id

    # Alias en MonitorPreguntasInactivas
    monitor = MonitorPreguntasInactivas(generador=generador)
    assert len(monitor.ejecutarRevision(preguntas=[p])) == 1


from unittest.mock import patch
from src.fabricas.fabrica_autor import FabricaAutor
from src.estrategia.estrategia_llm import EstrategiaLLM




def test_monitor_manejo_excepciones_db(session):
    cat = Categoria(nombre="Excepciones")
    autor = AgenteIA(nombre="ErrorBot")
    tag_ia = Tag(nombre="ia-help")
    p = Pregunta(titulo="Pregunta Error", cuerpo="Detalle", categoria=cat, autor=autor)
    p.tags.append(tag_ia)
    session.add_all([cat, autor, tag_ia, p])
    session.commit()

    generador = GeneradorRespuestaAutomatica(estrategia=EstrategiaLocal(), agente=autor)
    monitor = MonitorPreguntasInactivas(generador=generador)

    # Test rama except cuando falla la consulta general de preguntas
    with patch("src.models.pregunta.Pregunta.query") as mock_query:
        mock_query.all.side_effect = Exception("Fallo forzado en query")
        res = monitor.ejecutar_revision(preguntas=None)
        assert res == []

    # Test rama rollback cuando falla el commit
    with patch("src.extensions.db.session.commit", side_effect=Exception("Fallo forzado en commit")):
        with patch("src.extensions.db.session.rollback") as mock_rollback:
            monitor.ejecutar_revision(preguntas=[p], auto_commit=True)
            mock_rollback.assert_called_once()
