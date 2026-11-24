from .estrategia_llm import EstrategiaLLM


class EstrategiaGemini(EstrategiaLLM):
    """Estrategia concreta de generación de texto utilizando modelos de Google Gemini."""

    def __init__(self, modelo: str = "gemini-2.5-flash"):
        self.__modelo = modelo

    def generar(self, prompt: str) -> str:
        return f"[Gemini - {self.__modelo}] Respuesta generada para: {prompt}"