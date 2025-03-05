from .google_gemini_handler import GoogleGeminiHandler

def generate_search_query(prompt, url, llm_provider="google", **kwargs):
    """Generate a search query using an LLM."""
    if llm_provider == "google":
        handler = GoogleGeminiHandler(kwargs.get("llm_api_key"), kwargs.get("llm_name"))
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    full_prompt = f"Generate a search engine query for the prompt: {prompt}, related to the URL: {url}."
    return handler.generate_text(full_prompt, **kwargs)
