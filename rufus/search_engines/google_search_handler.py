from googlesearch import search
from .base_handler import SearchEngineHandler

class GoogleSearchHandler(SearchEngineHandler):
    def get_search_results(self, query, num_results=10):
        """Get search results from Google."""
        try:
            return list(search(query, num_results=num_results))
        except Exception as e:
            print(f"Error fetching Google search results: {e}")
            return []
