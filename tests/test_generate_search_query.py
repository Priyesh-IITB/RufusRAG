from rufus.llms.method import generate_search_query

def test_generate_search_query_with_google():
    config = {
        "llm_provider": "google",
        "llm_api_key": "AIzaSyAfn-WV-ZhcpT-GwpRY6J-FyQcMn5zlT14",
        "llm_name": "models/gemini-1.5-flash-latest"
    }
    prompt = "Find information about product features."
    url = "https://apple.com"
    query = generate_search_query(prompt, url, **config)
    assert isinstance(query, str)
    assert len(query) > 0
