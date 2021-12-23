import os

from fastapi import FastAPI

from typing import List, Optional

from RST_search import rst_search

app = FastAPI()

@app.post("/search")
def search(
    input_query: str = "Германия",
    selected_tags: Optional[List[str]] = ["NOUN"],
    selected_rels: Optional[List[str]] = ["contrast"]
):
    print("ok")
    return rst_search(input_query, selected_tags, selected_rels)