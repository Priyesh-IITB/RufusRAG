import pytest
from rufus.content_rankers.method import rank_content

@pytest.mark.parametrize("similarity_metric", ["cosine", "euclidean"])
def test_rank_content(similarity_metric):
    ref_text = ["How to fix Python errors"]
    candidate_texts = ["Python error solution", "Fix Python errors"]
    config = {
        "embd_model_provider": "google",
        "embd_model_api_key": "AIzaSyAfn-WV-ZhcpT-GwpRY6J-FyQcMn5zlT14",
        "embd_model_name": "models/text-embedding-004"
    }
    ranked_results = rank_content(ref_txt=ref_text, candidate_txt=candidate_texts, similarity_metric=similarity_metric, **config)
    assert len(ranked_results) == len(candidate_texts)
    assert all(isinstance(item, tuple) for item in ranked_results)
    assert all(isinstance(text, str) for text, _ in ranked_results)
    assert all(isinstance(score, (float, np.float32, np.float64)) for _, score in ranked_results)
