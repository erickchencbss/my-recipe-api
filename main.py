from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fuzzy_search import search_fuzzy

app = FastAPI()

class FuzzySearchRequest(BaseModel):
    pantry: List[str]
    top_k: int = 3

@app.post("/search/fuzzy")
def fuzzy_search(req: FuzzySearchRequest):
    return search_fuzzy(req.pantry, req.top_k)
