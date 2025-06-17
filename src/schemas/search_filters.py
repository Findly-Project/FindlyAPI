from typing import List
from pydantic import BaseModel


class SearchFilters(BaseModel):
    only_new: bool = False
    name_filter: bool = False
    price_filter: bool = False
    exclude_words: List[str] = []

    model_config = {"extra": "forbid"}

    def __eq__(self, other):
        if not isinstance(other, SearchFilters):
            return NotImplemented
        return all([self.only_new == other.only_new,
                    self.name_filter == other.name_filter,
                    self.price_filter == other.price_filter,
                    self.exclude_words == other.exclude_words])

    def __hash__(self):
        return hash((self.only_new, self.name_filter, self.price_filter, *self.exclude_words))