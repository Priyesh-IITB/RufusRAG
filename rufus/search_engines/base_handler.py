from abc import ABC, abstractmethod

class SearchEngineHandler(ABC):
    @abstractmethod
    def get_search_results(self, query, **kwargs):
        """Search the search engine for the given query."""
        pass
