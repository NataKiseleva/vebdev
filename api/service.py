import os

from fastapi import FastAPI, Query

from typing import List, Optional

from RST_search import rst_search, tags_abbs

tags = [tag[1] for tag in tags_abbs]

app = FastAPI()

@app.get("/search")
def search(
    input_query: str = Query("Германия"),
    selected_tag: Optional[str] = Query(None, enum=tags),
    selected_rels: Optional[List[str]] = Query(None)
):
    if selected_tag:
        selected_tags = [selected_tag]
    else:
        selected_tags = None
    return rst_search(input_query, selected_tags, selected_rels)
