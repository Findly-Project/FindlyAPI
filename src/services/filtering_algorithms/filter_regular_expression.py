import re
from src.services.product_parser.models.product_models import ProductsList


def regular_expression(query: str, candidates: ProductsList) -> ProductsList:
    clear_candidates: ProductsList = ProductsList()

    for candidate in candidates:
        is_best_result: bool = bool(
            re.match(rf"^(.*\s)?{query}(\s.*)?$", candidate.name, re.IGNORECASE)
        )

        if is_best_result:
            clear_candidates.add_product(candidate)

    return clear_candidates
