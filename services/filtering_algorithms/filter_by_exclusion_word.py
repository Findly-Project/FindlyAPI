from services.collecting_primary_data.product_models import ProductList


def filter_by_exclusion_word(exclusion_word: str, candidates: ProductList) -> ProductList:
    clear_candidates: ProductList = ProductList()

    for candidate in candidates:
        list_of_word: list[str] = [x.lower() for x in candidate.name.split()]
        if exclusion_word.lower().strip() in list_of_word:
            continue
        else:
            clear_candidates.add_product(candidate)

    return clear_candidates
