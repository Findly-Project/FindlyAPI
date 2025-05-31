from pydantic import BaseModel


class RequestArgs(BaseModel):
    q: str | None = None
    nf: str | None = None
    pf: str | None = None
    ms: str | None = None
    on: str | None = None
    ew: str | None = None