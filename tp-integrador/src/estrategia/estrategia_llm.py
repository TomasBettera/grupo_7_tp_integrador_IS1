from abc import ABC, abstractmethod


class EstrategiaLLM(ABC):
    """Contrato común para las estrategias de generación de texto mediante LLMs."""

    @abstractmethod
    def generar(self, prompt: str) -> str:
        """Genera una respuesta de texto a partir de un prompt."""
        pass