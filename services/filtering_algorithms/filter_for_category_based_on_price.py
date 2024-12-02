from ..collecting_primary_data.product_models import ProductList


def filter_by_price(candidates: ProductList) -> ProductList:
    if len(candidates) > 1:
        while True:
            is_filter: bool = True
            for i in range(len(candidates) - 1):
                try:
                    if candidates[i + 1].price / candidates[i].price > 2:
                        candidates.del_product(i)
                        is_filter: bool = False
                except IndexError:
                    continue

            if is_filter:
                return candidates
    else:
        return candidates
