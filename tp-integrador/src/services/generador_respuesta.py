from datetime import timedelta
from typing import Optional

from src.estrategia.estrategia_llm import EstrategiaLLM
from src.fabricas.fabrica_agente_ia import FabricaAgenteIA
from src.models.agente_ia import AgenteIA
from src.models.pregunta import Pregunta
from src.models.respuesta import Respuesta


class GeneradorRespuestaAutomatica:

    def __init__(
        self,
        estrategia: EstrategiaLLM,
        umbral_tiempo_espera: Optional[timedelta] = None,
        agente: Optional[AgenteIA] = None,
    ):
        self.estrategia = estrategia
        self.umbral_tiempo_espera = (
            umbral_tiempo_espera if umbral_tiempo_espera is not None else timedelta(hours=24)
        )
        if agente is None:
            fabrica = FabricaAgenteIA()
            self.agente = fabrica.crear_autor(nombre="Bot Asistente IA")
        else:
            self.agente = agente

    def debe_activarse(self, p: Pregunta) -> bool:
        tiene_tag_ia = p.tiene_etiqueta("ia-help") or p.tiene_etiqueta("#ia-help")
        inactiva = p.esta_sin_responder() and p.supero_tiempo_limite(self.umbral_tiempo_espera)
        return tiene_tag_ia or inactiva

    def debeActivarse(self, p: Pregunta) -> bool:
        return self.debe_activarse(p)

    def construir_prompt(self, p: Pregunta) -> str:
        categoria_info = f" [Categoría: {p.categoria.nombre}]" if p.categoria else ""
        return (
            f"Por favor responde de forma clara y precisa a la siguiente consulta universitaria{categoria_info}:\n"
            f"Título: {p.titulo}\n"
            f"Detalle: {p.cuerpo}"
        )

    def generar_para(self, p: Pregunta) -> Respuesta:
        prompt = self.construir_prompt(p)
        texto_generado = self.estrategia.generar(prompt)

        respuesta = Respuesta(
            cuerpo=texto_generado,
            pregunta=p,
            autor=self.agente,
        )
        p.agregar_respuesta(respuesta)
        return respuesta

    def generarPara(self, p: Pregunta) -> Respuesta:
        return self.generar_para(p)
