import os

from fastapi import FastAPI, Query

from typing import List, Optional

from RST_search import rst_search, tags_abbs, rels_abbs

all_tags = [tag[1] for tag in tags_abbs]
all_rels = [f"<i>{tag[1]}</i>" for tag in rels_abbs]

app = FastAPI(
    title = "RST corpus seach API",
    version = '0.1.0'
)

@app.get(
    "/search",
    description="Using this method you can search for a specific Russian or English word in parallel RST corpus. You can select a POS tag for disambiguation and specify discource relations you would like to see on that word",
    summary="Search a word in RST corpus"
)
def search(
    query: str = Query("Германия", description="A Russian or English word you would like to search"),
    tag: Optional[str] = Query(None, enum=all_tags, description="(Optional) POS tag of the given word "),
    rels: Optional[List[str]] = Query(None, description=f"(Optional) Type of discourse relation - one or multiple (logical OR) from: {', '.join(all_rels)}")
):
    if tag:
        tags = [tag]
    else:
        tags = None
    return rst_search(query, tags, rels)
