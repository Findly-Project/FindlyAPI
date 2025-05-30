from services.collecting_primary_data.product_models import ProductList


def filter_by_exclusion_words(exclusion_words: list[str], candidates: ProductList) -> ProductList:
    clear_candidates: ProductList = ProductList()
    exclusion_words = set([x.lower().strip() for x in exclusion_words])

    for candidate in candidates:
        list_of_word: set[str] = set([x.lower() for x in candidate.name.split()])
        if len(list_of_word.intersection(exclusion_words)) > 0:
            continue
        else:
            clear_candidates.add_product(candidate)

    return clear_candidates
