from types import NoneType
from .collecting_primary_data.get_kufar_data import get_kufar_data
from .collecting_primary_data.get_mmg_data import get_mmg_data
from .collecting_primary_data.get_onliner_data import get_onliner_data
from .collecting_primary_data.get_21vek_data import get_21vek_data
from .collecting_primary_data.product_models import (
    ProductList,
    MarketPlaceList,
    SortAndFilterProductList,
)
from services.filtering_algorithms import (
    filter_regular_expression,
    filter_for_category_based_on_price,
    filter_by_exclusion_word
)
from typing import Dict, List
from aiocache import cached
from aiocache.serializers import PickleSerializer
from httpx import RemoteProtocolError, TimeoutException


@cached(ttl=5 * 60, serializer=PickleSerializer())
async def output_of_results(
    query: str,
    max_size: int | None,
    only_new: bool,
    enable_filter_by_price: bool,
    enable_filter_by_name: bool,
    exclusion_word: str | bool,
) -> MarketPlaceList:
    if max_size in [None, NoneType]:
        max_size = 10
    elif max_size == 0:
        max_size = 40

    get_data_functions: Dict[str, query] = {
        "Kufar": get_kufar_data,
        "MMG": get_mmg_data,
        "21vek": get_21vek_data,
        "Onliner": get_onliner_data,
    }
    output_result_items: MarketPlaceList = MarketPlaceList()

    for func_name, func in get_data_functions.items():
        try:
            match func_name:
                case "Kufar":
                    pars_data: ProductList = await func(query=query, only_new=only_new)
                case _:
                    pars_data: ProductList = await func(query=query)
        except (RemoteProtocolError, TimeoutException):
            match func_name:
                case "Kufar":
                    pars_data: ProductList = await func(query=query, only_new=only_new)
                case _:
                    pars_data: ProductList = await func(query=query)

        if isinstance(exclusion_word, str):
            items_filtered_by_exclusion_word = filter_by_exclusion_word.filter_by_exclusion_word(exclusion_word, pars_data)
        else:
            items_filtered_by_exclusion_word: ProductList = pars_data

        if not enable_filter_by_name:
            items_sorted_by_price: ProductList = items_filtered_by_exclusion_word
        else:
            product_names: List[str] = [j.name for j in items_filtered_by_exclusion_word]

            items_filtered_by_regular_expression: List[str] = (
                filter_regular_expression.regular_expression(query, product_names)
            )
            items_filtered_by_name: ProductList = (
                SortAndFilterProductList.filter_by_name(
                    items_filtered_by_regular_expression, pars_data
                )
            )
            items_sorted_by_price: ProductList = SortAndFilterProductList.sort_by_price(
                items_filtered_by_name
            )

        if not enable_filter_by_price:
            result_items = items_sorted_by_price
        else:
            result_items: ProductList = (
                filter_for_category_based_on_price.filter_by_price(
                    items_sorted_by_price
                )
            )
        if len(result_items) > max_size:
            result_items: ProductList = ProductList(result_items[:max_size])
        if result_items:
            output_result_items.add_list_of_products(func_name, result_items)

    return output_result_items
