import re
from services.collecting_primary_data.product_models import ProductList


def regular_expression(query: str, candidates: ProductList) -> ProductList:
    clear_candidates: ProductList = ProductList()

    for candidate in candidates:
        is_best_result: bool = bool(
            re.match(rf"^(.*\s)?{query}(\s.*)?$", candidate.name, re.IGNORECASE)
        )

        if is_best_result:
            clear_candidates.add_product(candidate)

    return clear_candidates
