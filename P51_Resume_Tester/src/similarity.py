"""U3 - Confirm pairs are equivalent.

Two checks (only the strict one aborts a run; a low cosine is reported as a warning,
because sentence embeddings move when a name changes even if the resume is equivalent):
 1. STRICT: after masking name/email/hometown, both resumes are string-identical.
 2. SEMANTIC: BERT-family sentence-embedding cosine similarity >= threshold.
    Falls back to character-3-gram TF-IDF cosine if sentence-transformers or the
    model weights are unavailable (the method used is recorded in the output).
"""
import math
from collections import Counter
import numpy as np
from .resumes import mask_text

def _tfidf_embed(texts):
    grams = [Counter(t[i:i+3] for i in range(len(t) - 2)) for t in texts]
    df = Counter(g for c in grams for g in c)
    n = len(texts)
    vocab = {g: i for i, g in enumerate(sorted(df))}
    M = np.zeros((n, len(vocab)))
    for r, c in enumerate(grams):
        for g, f in c.items():
            M[r, vocab[g]] = (1 + math.log(f)) * (math.log((1 + n) / (1 + df[g])) + 1)
    return M

def embed(texts, mode="auto", bert_model="sentence-transformers/all-MiniLM-L6-v2"):
    if mode in ("auto", "bert"):
        try:
            from sentence_transformers import SentenceTransformer
            m = SentenceTransformer(bert_model)
            return np.asarray(m.encode(texts, normalize_embeddings=True)), f"BERT ({bert_model})"
        except Exception as e:
            if mode == "bert":
                raise
    return _tfidf_embed(texts), "FALLBACK: char-3gram TF-IDF (no BERT available)"

def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

def check_pairs(rows, mode="auto", bert_model=None, min_sim=None):
    """rows: list of dicts with pair_id, base_text, var_text, base_name, base_hometown, var_name, var_hometown."""
    kw = {"bert_model": bert_model} if bert_model else {}
    texts = [t for r in rows for t in (r["base_text"], r["var_text"])]
    E, method = embed(texts, mode, **kw)
    if min_sim is None:   # TF-IDF cosine runs lower than BERT on tiny corpora
        min_sim = 0.80 if method.startswith("BERT") else 0.85
    out = []
    for i, r in enumerate(rows):
        sim = cos(E[2 * i], E[2 * i + 1])
        mb = mask_text(r["base_text"], r["base_name"], r["base_hometown"])
        mv = mask_text(r["var_text"], r["var_name"], r["var_hometown"])
        strict = mb == mv
        out.append(dict(pair_id=r["pair_id"], cosine=round(sim, 4), masked_identical=strict,
                        embedding_ok=bool(sim >= min_sim), equivalent=bool(strict)))
    return out, method, min_sim
