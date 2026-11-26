from datetime import datetime, timedelta

from src.estrategia.estrategia_gemini import EstrategiaGemini
from src.models.agente_ia import AgenteIA
from src.models.categoria import Categoria
from src.models.pregunta import Pregunta
from src.models.tag import Tag
from src.services.generador_respuesta import GeneradorRespuestaAutomatica
from src.services.monitor_preguntas import MonitorPreguntasInactivas


def test_monitor_ejecutar_revision(session):
    cat = Categoria(nombre="Algoritmos")
    tag_ia = Tag(nombre="ia-help")
    autor = AgenteIA(nombre="Estudiante 1")
    bot = AgenteIA(nombre="Bot Oficial")
    session.add_all([cat, tag_ia, autor, bot])
    session.commit()

    p1 = Pregunta(titulo="P1 Normal", cuerpo="Cuerpo 1", categoria=cat, autor=autor)

    hace_tres_dias = datetime.now() - timedelta(days=3)
    p2 = Pregunta(
        titulo="P2 Inactiva",
        cuerpo="Cuerpo 2",
        categoria=cat,
        autor=autor,
        fecha_publicacion=hace_tres_dias,
    )

    p3 = Pregunta(titulo="P3 Con Tag", cuerpo="Cuerpo 3", categoria=cat, autor=autor)
    p3.tags.append(tag_ia)

    session.add_all([p1, p2, p3])
    session.commit()

    generador = GeneradorRespuestaAutomatica(
        estrategia=EstrategiaGemini(),
        umbral_tiempo_espera=timedelta(hours=24),
        agente=bot,
    )
    monitor = MonitorPreguntasInactivas(
        generador=generador, intervalo_chequeo=timedelta(hours=1)
    )

    respuestas = monitor.ejecutar_revision(auto_commit=True)

    assert len(respuestas) == 2
    assert len(p1.respuestas) == 0
    assert len(p2.respuestas) == 1
    assert len(p3.respuestas) == 1

    assert p2.respuestas[0].autor_id == bot.id
    assert p3.respuestas[0].autor_id == bot.id