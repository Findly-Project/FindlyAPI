from ..collecting_primary_data.product_models import ProductList, SortProductList


def filter_by_price(candidates: ProductList) -> ProductList:
    items_sorted_by_price: ProductList = SortProductList.sort_by_price(candidates)
    if len(items_sorted_by_price) > 1:
        while True:
            is_filter: bool = True
            for i in range(len(items_sorted_by_price) - 1):
                try:
                    if (
                        items_sorted_by_price[i + 1].price
                        / items_sorted_by_price[i].price
                        > 2
                    ):
                        items_sorted_by_price.del_product(i)
                        is_filter: bool = False
                except IndexError:
                    continue

            if is_filter:
                return items_sorted_by_price
    else:
        return items_sorted_by_price
