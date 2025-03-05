from abc import ABC, abstractmethod

class LLMHandler(ABC):
    @abstractmethod
    def generate_text(self, prompt, **kwargs):
        """Generate text based on the provided prompt."""
        pass
