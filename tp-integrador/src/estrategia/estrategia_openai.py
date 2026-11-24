from .estrategia_llm import EstrategiaLLM


class EstrategiaOpenAI(EstrategiaLLM):
    """Estrategia concreta de generación de texto utilizando modelos de OpenAI."""

    def __init__(self, modelo: str = "gpt-4o-mini"):
        self.__modelo = modelo

    def generar(self, prompt: str) -> str:
        return f"[OpenAI - {self.__modelo}] Respuesta generada para: {prompt}"