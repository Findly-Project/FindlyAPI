import re

from src.services.product_parser.models.product_models import ProductsList, Product


class Filter:
    def __init__(self, pars_data: ProductsList):
        self.pars_data = pars_data

    def by_price(self) -> None:
        result_items: list[Product] = self.pars_data.get_sorted_products()
        if len(result_items) > 1:
            while True:
                is_filter: bool = True
                for i in range(len(result_items) - 1):
                    try:
                        if result_items[i + 1].price / result_items[i].price > 2:
                            result_items.pop(i)
                            is_filter: bool = False
                    except IndexError:
                        continue

                if is_filter:
                    self.pars_data = result_items
                    return
        else:
            self.pars_data = result_items
            return

    def by_name(self, query: str):
        result_items: ProductsList = ProductsList()
        for candidate in self.pars_data:
            is_best_result: bool = bool(re.match(rf"^(.*\s)?{query}(\s.*)?$", candidate.name, re.IGNORECASE))
            if is_best_result:
                result_items.add_product(candidate)

        self.pars_data = result_items

    def by_exclude_words(self, exclude_words: list[str]):
        result_items: ProductsList = ProductsList()
        exclusion_words = set([x.lower().strip() for x in exclude_words])

        for candidate in self.pars_data:
            list_of_word: set[str] = set([x.lower() for x in candidate.name.split()])
            if len(list_of_word.intersection(exclusion_words)) > 0:
                continue
            else:
                result_items.add_product(candidate)

        self.pars_data = result_items

    def get_filtering_products(self) -> ProductsList:
        return ProductsList(products=self.pars_data.get_sorted_products())
