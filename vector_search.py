from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Define sample recipes
recipes = [
    {"title": "Pancakes", "ingredients": ["milk", "flour", "eggs", "baking powder"]},
    {"title": "Scrambled Eggs", "ingredients": ["eggs", "butter", "salt"]},
    {"title": "Avocado Toast", "ingredients": ["bread", "avocado", "salt", "pepper"]},
    {"title": "Grilled Cheese", "ingredients": ["bread", "cheese", "butter"]},
]

# 3. Convert each recipe to a string and embed
texts = [" ".join(recipe["ingredients"]) for recipe in recipes]
vectors = model.encode(texts, convert_to_numpy=True)

# 4. Build FAISS index
d = vectors.shape[1]  # dimension
index = faiss.IndexFlatL2(d)
index.add(vectors)

# 5. User pantry input
user_pantry = ["eggs", "milk", "butter"]
query = " ".join(user_pantry)
query_vec = model.encode([query], convert_to_numpy=True)

# 6. Search
k = 3  # top 3 matches
distances, indices = index.search(query_vec, k)

# 7. Print results
print("Top matches:")
for i in indices[0]:
    print(f"- {recipes[i]['title']} ({recipes[i]['ingredients']})")
