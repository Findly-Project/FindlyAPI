from pydantic import BaseModel, Field


class SearchFilters(BaseModel):
    only_new: bool = Field(default=False, strict=True, description="Only new products from Kufar in response")
    name_filter: bool = Field(default=False, strict=True, description="Ensures that the search keyword is contained in the name of each product in the response")
    price_filter: bool = Field(default=False, strict=True, description="Enable price filtering")
    exclude_words: tuple[str, ...] = Field(default=(), description="Ensures that the name of each product in the answer will not contain any of the excluded words")

    model_config = {"extra": "forbid", "frozen": True}
