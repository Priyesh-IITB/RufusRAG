import numpy as np
from rufus.utils import cosine_similarity, pairwise_distance
from .google_text_embedding_reranker import GoogleTextEmbeddingReranker

def rank_content(ref_txt, candidate_txt, similarity_metric="cosine", embd_model_provider="google", **kwargs):
    """Rank content based on similarity to reference text."""
    if embd_model_provider == "google":
        reranker = GoogleTextEmbeddingReranker(kwargs.get("embd_model_api_key"), kwargs.get("embd_model_name"))
    else:
        raise ValueError(f"Unsupported provider: {embd_model_provider}")
    
    ref_embeddings = reranker.get_embeddings(ref_txt)
    candidate_embeddings = reranker.get_embeddings(candidate_txt)
    
    if not ref_embeddings or not candidate_embeddings:
        return []
    
    if similarity_metric == "cosine":
        scores = cosine_similarity(ref_embeddings, candidate_embeddings)
    elif similarity_metric == "euclidean":
        scores = pairwise_distance(ref_embeddings, candidate_embeddings)
    else:
        raise ValueError(f"Unknown similarity metric: {similarity_metric}")
    
    ranked_content = sorted(zip(candidate_txt, scores), key=lambda x: x[1], reverse=True)
    return ranked_content
