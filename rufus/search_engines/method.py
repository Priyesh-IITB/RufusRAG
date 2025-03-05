from .google_search_handler import GoogleSearchHandler

def get_search_results(query, search_engine="google", num_results=10, **kwargs):
    """Retrieve search results."""
    if search_engine == "google":
        handler = GoogleSearchHandler()
    else:
        raise ValueError(f"Unsupported search engine: {search_engine}")
    return handler.get_search_results(query, num_results=num_results)
