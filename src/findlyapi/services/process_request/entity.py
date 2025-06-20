from aiocache import cached
from aiocache.serializers import PickleSerializer

from findlyapi.schemas.search_payload import SearchPayload
from findlyapi.services.filter.entity import Filter
from findlyapi.services.product_parser.entity import ProductParser
from findlyapi.services.product_parser.models.product_models import ProductsList, NamedProductsList
from findlyapi.utils.key_from_instance_hash import key_from_instance_hash


class ProcessRequest:
    def __init__(self, search_params: SearchPayload):
        self.search_params = search_params

    @cached(ttl=5 * 60, serializer=PickleSerializer(), key_builder=key_from_instance_hash)
    async def get_response(self) -> list[NamedProductsList]:
        product_lists: list[NamedProductsList] = []
        product_parser: ProductParser = ProductParser(self.search_params.query)

        if "Onliner" not in self.search_params.exclude_marketplaces:
            onliner_data: ProductsList = await product_parser.get_onliner_data()
            product_lists.append(self._filter_pars_data(onliner_data, 'Onliner'))

        if "MMG" not in self.search_params.exclude_marketplaces:
            mmg_data: ProductsList = await product_parser.get_mmg_data()
            product_lists.append(self._filter_pars_data(mmg_data, 'MMG'))

        if "Kufar" not in self.search_params.exclude_marketplaces:
            kufar_data: ProductsList = await product_parser.get_kufar_data(self.search_params.filters.only_new)
            product_lists.append(self._filter_pars_data(kufar_data, 'Kufar'))

        if "21vek" not in self.search_params.exclude_marketplaces:
            _21vek_data: ProductsList = await product_parser.get_21vek_data()
            product_lists.append(self._filter_pars_data(_21vek_data, '21vek'))

        return product_lists

    def _filter_pars_data(self, pars_data: ProductsList, marketplace: str) -> NamedProductsList:
        filters = self.search_params.filters.model_dump()
        max_size = self.search_params.max_size
        filter_data = Filter(pars_data)

        filter_data.by_exclude_words(filters['exclude_words'])

        if filters['price_filter']['is_enabled']:
            filter_data.by_price(filters['price_filter']['tolerance'])

        if filters['name_filter']:
            filter_data.by_name(self.search_params.query)

        if size_products := len(filter_data.get_filtering_products()) > max_size.size:
            if max_size.max_or_min_cut == "min":
                return NamedProductsList(marketplace, filter_data.get_filtering_products()[:max_size.size])
            elif max_size.max_or_min_cut == "max":
                return NamedProductsList(marketplace, filter_data.get_filtering_products()[size_products - max_size.size - 1:])
            else:
                return NamedProductsList(marketplace, ProductsList())
        else:
            return NamedProductsList(marketplace, filter_data.get_filtering_products())

    def __eq__(self, other):
        if not isinstance(other, ProcessRequest):
            return NotImplemented
        return self.search_params == other.search_params

    def __hash__(self):
        return hash(self.search_params)
