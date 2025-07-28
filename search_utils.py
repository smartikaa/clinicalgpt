from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd

# Load and embed trials
def setup_index(data_path="trials.json"):
    df = pd.read_json(data_path)
    df['text'] = df.apply(lambda r: f"{r.condition} {r.phase} {r.masking} {r.location} {r.age_range} {r.sponsor}", axis=1)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df['text'].tolist(), convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return df, model, index

def semantic_search(filters, df, model, index, k=3):
    query = " ".join(str(v) for v in filters.values() if v)
    query_vec = model.encode([query])

    D, I = index.search(query_vec, k)
    return df.iloc[I[0]]

