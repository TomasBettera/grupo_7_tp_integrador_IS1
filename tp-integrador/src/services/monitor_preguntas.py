from datetime import timedelta
from typing import List, Optional

from src.extensions import db
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta
from src.services.generador_respuesta import GeneradorRespuestaAutomatica


class MonitorPreguntasInactivas:

    def __init__(
        self,
        generador: GeneradorRespuestaAutomatica,
        intervalo_chequeo: Optional[timedelta] = None,
    ):
        self.generador = generador
        self.intervalo_chequeo = (
            intervalo_chequeo if intervalo_chequeo is not None else timedelta(minutes=60)
        )

    def ejecutar_revision(
        self, preguntas: Optional[List[Pregunta]] = None, auto_commit: bool = False
    ) -> List[Respuesta]:
        if preguntas is None:
            # Consulta a la base de datos relacional si está en contexto Flask
            try:
                preguntas = Pregunta.query.all()
            except Exception:
                preguntas = []

        respuestas_generadas: List[Respuesta] = []

        for p in preguntas:
            if self.generador.debe_activarse(p):
                nueva_respuesta = self.generador.generar_para(p)
                respuestas_generadas.append(nueva_respuesta)
                if auto_commit:
                    try:
                        db.session.add(nueva_respuesta)
                    except Exception:
                        pass

        if auto_commit and respuestas_generadas:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

        return respuestas_generadas

    def ejecutarRevision(
        self, preguntas: Optional[List[Pregunta]] = None, auto_commit: bool = False
    ) -> List[Respuesta]:
        return self.ejecutar_revision(preguntas=preguntas, auto_commit=auto_commit)
