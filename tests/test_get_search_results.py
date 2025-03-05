from rufus.search_engines.method import get_search_results

def test_get_search_results_with_google():
    query = "Best practices for web crawling"
    results = get_search_results(query, search_engine="google", num_results=3)
    assert isinstance(results, list)
    assert len(results) <= 3
    assert all(isinstance(result, str) for result in results)
