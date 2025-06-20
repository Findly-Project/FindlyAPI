import re
from typing import Literal

from pydantic import BaseModel, field_validator, model_validator, Field

from findlyapi.schemas.search_filters import SearchFilters


class MaxSize(BaseModel):
    size: int = Field(strict=True, default=20, description="Max size for search")
    max_or_min_cut: Literal["max", "min"] = Field(default="min", description="Max or min cut in response")

    @field_validator("size", mode='after')
    def validate_price(cls, value):
        if not (10 <= value <= 40):
            raise ValueError("Incorrect max size of products")
        return value

    model_config = {"extra": "forbid", "frozen": True}

class SearchPayload(BaseModel):
    query: str = Field(strict=True, description="Key phrase for search")
    max_size: MaxSize = Field(strict=True, default=MaxSize(), description="Max size for search")
    exclude_marketplaces: tuple[Literal["MMG", "Onliner", "Kufar", "21vek"], ...] = Field(description="Exclude marketplaces when searching", default=())
    filters: SearchFilters = Field(default=SearchFilters(), description="Search filters")

    @field_validator('query', mode='after')
    def normalize_and_validate_query(cls, value: str) -> str:
        if len(value) > 20:
            raise ValueError('Query too long, max length is 20')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9- ]*$', value):
            raise ValueError('The search query must contain letters, numbers or a minus sign')
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
                raise ValueError('When the filter by name is enabled, there cannot be an intersection between excluded words and query words')
        return self

    model_config = {"extra": "forbid", "frozen": True}


