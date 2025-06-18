from pydantic import BaseModel


class SearchFilters(BaseModel):
    only_new: bool = False
    name_filter: bool = False
    price_filter: bool = False
    exclude_words: tuple[str, ...] = ()

    model_config = {"extra": "forbid", "frozen": True}
