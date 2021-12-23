import os

from fastapi import FastAPI, Query

from typing import List, Optional

from RST_search import rst_search, tags_abbs, rels_abbs

tags = [tag[1] for tag in tags_abbs]
rels = [f"<i>{tag[1]}</i>" for tag in rels_abbs]

app = FastAPI()

@app.get("/search")
def search(
    input_query: str = Query("Германия", description="A Russian or English word you would like to search"),
    selected_tag: Optional[str] = Query(None, enum=tags, description="(Optional) POS tag of the given word "),
    selected_rels: Optional[List[str]] = Query(None, description=f"(Optional) Type of discourse relation - one or multiple from: {', '.join(rels)}")
):
    if selected_tag:
        selected_tags = [selected_tag]
    else:
        selected_tags = None
    return rst_search(input_query, selected_tags, selected_rels)
