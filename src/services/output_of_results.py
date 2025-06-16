from types import NoneType
from src.services.product_parser.models.product_models import (
    ProductsList,
    MarketPlaceList,
)
from src.schemas.search_payload import SearchPayload
from src.services.filter import (
    filter_regular_expression,
    filter_for_category_based_on_price,
    filter_by_exclusion_word,
)
from aiocache import cached
from aiocache.serializers import PickleSerializer
from httpx import RemoteProtocolError, TimeoutException


@cached(ttl=5 * 60, serializer=PickleSerializer())
async def output_of_results(search_params: SearchPayload) -> MarketPlaceList:
    if max_size in [None, NoneType]:
        max_size: int = 10
    elif max_size == 0:
        max_size: int = 40

    get_data_functions: dict[str, query] = {
        "Kufar": get_kufar_data,
        "MMG": get_mmg_data,
        "21vek": get_21vek_data,
        "Onliner": get_onliner_data,
    }
    output_result_items: MarketPlaceList = MarketPlaceList()

    for func_name, func in get_data_functions.items():
        pars_data: ProductsList = await get_data_from_func(
            func_name, query, only_new, func
        )

        if isinstance(exclude_words, list):
            items_filtered_by_exclusion_word: ProductsList = (
                filter_by_exclusion_word.filter_by_exclusion_words(
                    exclude_words, pars_data
                )
            )
        else:
            items_filtered_by_exclusion_word: ProductsList = pars_data
        if not price_filter:
            result_items = items_filtered_by_exclusion_word
        else:
            result_items: ProductsList = (
                filter_for_category_based_on_price.filter_by_price(
                    items_filtered_by_exclusion_word
                )
            )

        if not name_filter:
            items_sorted_by_price: ProductsList = SortProductList.sort_by_price(
                result_items
            )
        else:
            items_filtered_by_regular_expression: ProductsList = (
                filter_regular_expression.regular_expression(query, result_items)
            )
            items_sorted_by_price: ProductsList = SortProductList.sort_by_price(
                items_filtered_by_regular_expression
            )

        if len(items_sorted_by_price) > max_size:
            items_sorted_by_price: ProductsList = ProductsList(
                items_sorted_by_price[:max_size]
            )
        if items_sorted_by_price.products:
            output_result_items.add_list_of_products(func_name, items_sorted_by_price)

    return output_result_items


async def get_data_from_func(marketplace, query, only_new, func):
    try:
        match marketplace:
            case "Kufar":
                pars_data: ProductsList = await func(query=query, only_new=only_new)
            case _:
                pars_data: ProductsList = await func(query=query)
        return pars_data

    except (RemoteProtocolError, TimeoutException):
        match marketplace:
            case "Kufar":
                pars_data: ProductsList = await func(query=query, only_new=only_new)
            case _:
                pars_data: ProductsList = await func(query=query)
        return pars_data
