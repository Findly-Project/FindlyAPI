from pydantic import BaseModel, field_validator

from fastapi import Query


class RequestArgs(BaseModel):
    q: str | None = Query(default=None, title="query", description="Query string")
    nf: str | None = Query(default=None, title="name filter")
    pf: str | None = Query(default=None, title="price filter")
    ms: str | None = Query(default=None, title="max size")
    on: str | None = Query(default=None, title="only new")
    ew: str | None = Query(default=None, title="exclusion words")
