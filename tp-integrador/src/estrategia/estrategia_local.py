from .estrategia_llm import EstrategiaLLM


class EstrategiaLocal(EstrategiaLLM):
    """Estrategia concreta de generación de texto utilizando un modelo local."""

    def __init__(self, modelo: str = "llama3"):
        self.__modelo = modelo

    def generar(self, prompt: str) -> str:
        return f"[Local - {self.__modelo}] Respuesta generada para: {prompt}"