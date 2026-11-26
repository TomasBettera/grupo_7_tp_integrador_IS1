from src.estrategia.estrategia_llm import EstrategiaLLM


class EstrategiaGemini(EstrategiaLLM):
    def __init__(self, modelo: str = "gemini-3.8-flash"):
        self.modelo = modelo

    def generar(self, prompt: str) -> str:
        return f"[Gemini - {self.modelo}] Respuesta generada para: {prompt}"
    