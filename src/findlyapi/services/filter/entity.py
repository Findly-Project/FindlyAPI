import re

from findlyapi.services.product_parser.models.product_models import ProductsList, Product


class Filter:
    def __init__(self, pars_data: ProductsList):
        self.pars_data: ProductsList = pars_data

    def by_price(self, tolerance: float) -> None:
        result_items: list[Product] = self.pars_data.get_sorted_by_price_products()
        if len(result_items) == 0:
            self.pars_data = ProductsList()

        n = len(result_items)
        dp = [1] * n
        prev_idx = [-1] * n

        for i in range(1, n):
            for j in range(i):
                if abs(result_items[i].price - result_items[j].price) <= tolerance * result_items[j].price:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        prev_idx[i] = j
        max_len_idx = 0
        if n > 0:
            max_len = dp[0]
            for i in range(1, n):
                if dp[i] > max_len:
                    max_len = dp[i]
                    max_len_idx = i
        sequence = []
        current_idx = max_len_idx
        while current_idx != -1:
            sequence.append(result_items[current_idx])
            current_idx = prev_idx[current_idx]

        self.pars_data = ProductsList(products=sequence[::-1])

    def by_name(self, query: str):
        result_items: ProductsList = ProductsList()
        for candidate in self.pars_data.products:
            is_best_result: bool = bool(re.match(rf"^(.*\s)?{query}(\s.*)?$", candidate.name, re.IGNORECASE))
            if is_best_result:
                result_items.add_product(candidate)

        self.pars_data = result_items

    def by_exclude_words(self, exclude_words: list[str]):
        result_items: ProductsList = ProductsList()
        exclusion_words = set([x.lower().strip() for x in exclude_words])

        for candidate in self.pars_data.products:
            list_of_word: set[str] = set([x.lower() for x in candidate.name.split()])
            if len(list_of_word.intersection(exclusion_words)) > 0:
                continue
            else:
                result_items.add_product(candidate)

        self.pars_data = result_items

    def get_filtering_products(self) -> ProductsList:
        return ProductsList(products=self.pars_data.get_sorted_by_price_products())
