"""
Embed persona+task and rank PDF sections based on semantic similarity.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def load_model(model_path="models/all-MiniLM-L6-v2"):
    return SentenceTransformer(model_path)


def rank_sections(sections, prompt_text, model, top_k=5):
    section_texts = [s["section_text"] for s in sections]
    prompt_embedding = model.encode([prompt_text])
    section_embeddings = model.encode(section_texts)

    sims = cosine_similarity(prompt_embedding, section_embeddings)[0]
    scored = sorted(zip(sims, sections), key=lambda x: x[0], reverse=True)[:top_k]

    return [
        {
            "document": s["document"],
            "section_title": s["section_title"],
            "importance_rank": i + 1,
            "page_number": s["page_number"],
            "section_text": s["section_text"]
        }
        for i, (score, s) in enumerate(scored)
    ]
