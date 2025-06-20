from pydantic import BaseModel, Field, model_validator


class PriceFilter(BaseModel):
    is_enabled: bool = Field(default=False, strict=True, description="Enable price filtering")
    tolerance: float = Field(default=0.5, strict=True, description="Tolerance for price filtering")

    @model_validator(mode='after')
    def validate_enabling_price_filter(self):
        if not self.is_enabled:
            if "tolerance" in self.model_fields_set:
                raise ValueError("Price filter tolerance can only be used with enabled Price filter")
        return self

    model_config = {"extra": "forbid", "frozen": True}


class SearchFilters(BaseModel):
    only_new: bool = Field(default=False, strict=True, description="Only new products from Kufar in response")
    name_filter: bool = Field(default=False, strict=True, description="Ensures that the search keyword is contained in the name of each product in the response")
    price_filter: PriceFilter = Field(default=PriceFilter(), strict=True, description="Configuring price filter")
    exclude_words: tuple[str, ...] = Field(default=(), description="Ensures that the name of each product in the answer will not contain any of the excluded words")

    model_config = {"extra": "forbid", "frozen": True}
