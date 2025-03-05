from abc import ABC, abstractmethod

class BaseReranker(ABC):
    @abstractmethod
    def get_embeddings(self, texts):
        """Obtain embeddings for the given list of texts."""
        pass
