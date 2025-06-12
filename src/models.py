import re
from typing import List
from pydantic import BaseModel, field_validator, model_validator


class SearchFilters(BaseModel):
    only_new: bool = False
    name_filter: bool = False
    price_filter: bool = False
    exclude_words: List[str] = []

    model_config = {"extra": "forbid"}


class SearchPayload(BaseModel):
    query: str
    max_size: int = 20
    filters: SearchFilters = SearchFilters()

    @field_validator('query', mode='before')
    def normalize_and_validate_query(cls, value: str) -> str:
        if len(value) > 20:
            raise ValueError('Query too long, max length is 20')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9-]*$', value):
            raise ValueError('The search query must contain letters, numbers or a minus sign')
        transformed_query = value.strip().replace(' ', '+')
        return transformed_query

    @field_validator("max_size", mode='before')
    def validate_price(cls, value):
        if not (10 <= value <= 40):
            raise ValueError("Incorrect max size of products")
        return value

    @model_validator(mode='after')
    def check_name_filter_logic(self):
        enable_name_filter = self.filters.name_filter
        query = self.query
        exclusion_words = self.filters.exclude_words
        if enable_name_filter and exclusion_words:
            set_query: set[str] = set(x.lower() for x in query.split())
            set_exclusion_words: set[str] = set(x.lower() for x in exclusion_words)
            if len(set_query.intersection(set_exclusion_words)) > 0:
                raise ValueError('When the filter by name is enabled, there cannot be an intersection between excluded words and query words.')
        return self

    model_config = {"extra": "forbid"}
