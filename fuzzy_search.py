from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=os.getenv("HF_HOME", None))

recipes = [
    {"title": "Pancakes", "ingredients": ["milk", "flour", "eggs", "baking powder"]},
    {"title": "Scrambled Eggs", "ingredients": ["eggs", "butter", "salt"]},
    {"title": "Avocado Toast", "ingredients": ["bread", "avocado", "salt", "pepper"]},
    {"title": "Grilled Cheese", "ingredients": ["bread", "cheese", "butter"]},
]

texts = [" ".join(r["ingredients"]) for r in recipes]
vectors = model.encode(texts, convert_to_numpy=True)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

def search_fuzzy(pantry: list[str], k: int = 5):
    pantry_set = set(i.lower() for i in pantry)
    query_str = " ".join(pantry)
    query_vec = model.encode([query_str], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)

    results = []
    for i, dist in zip(indices[0], distances[0]):
        recipe = recipes[i]
        recipe_ingredients = set(ing.lower() for ing in recipe["ingredients"])

        # Components of hybrid score
        semantic_sim = 1 / (1 + dist)
        literal_overlap = len(pantry_set & recipe_ingredients) / len(recipe_ingredients)

        # Weighted score
        final_score = 0.7 * semantic_sim + 0.3 * literal_overlap

        results.append({
            "title": recipe["title"],
            "ingredients": recipe["ingredients"],
            "semantic": round(float(semantic_sim), 4),
            "overlap": round(float(literal_overlap), 4),
            "score": round(float(final_score), 4)
        })


    # Return sorted by final score descending
    return sorted(results, key=lambda x: x["score"], reverse=True)
