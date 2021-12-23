import os

from fastapi import FastAPI, Query

from typing import List, Optional

from RST_search import rst_search, tags_abbs, rels_abbs

app = FastAPI()

@app.get("/search")
def search(
    input_query: str = Query("Германия"),
    selected_tags: Optional[List[str]] = Query(None),
    selected_rels: Optional[List[str]] = Query(None)
):
    print("ok")
    return rst_search(input_query, selected_tags, selected_rels)
