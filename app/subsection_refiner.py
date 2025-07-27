"""
Extract most relevant paragraphs from a section based on similarity to persona+task.
"""

import re
from sklearn.metrics.pairwise import cosine_similarity


def extract_best_paragraphs(section_text, prompt_text, model, top_k=1):
    paragraphs = [p.strip() for p in re.split(r'\\n{2,}', section_text) if p.strip()]
    if not paragraphs:
        return section_text

    para_embeddings = model.encode(paragraphs)
    prompt_embedding = model.encode([prompt_text])
    scores = cosine_similarity(prompt_embedding, para_embeddings)[0]

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    top_paragraphs = [paragraphs[i] for i in top_indices]

    return "\n\n".join(top_paragraphs) if top_paragraphs else section_text
