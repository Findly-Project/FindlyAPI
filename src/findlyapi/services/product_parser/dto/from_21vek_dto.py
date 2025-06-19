import json
import re
from httpx import Response

from findlyapi.services.product_parser.dto.base_from_dto import BaseFromDTO
from findlyapi.services.product_parser.models.product_models import ProductsList, Product


class From21vekDTO(BaseFromDTO):
    def __init__(self, pars_data: Response, first_part_url: str):
        self.pars_data: str = pars_data.text
        self.first_part_url: str = first_part_url

    def __call__(self) -> ProductsList:
        product_list: ProductsList = ProductsList()
        data: dict = json.loads(self.pars_data)
        data: dict = list(filter(lambda x: x.get('group_type') == 'products', data['data']))[0]

        for i in data.get('items', []):
            item: Product = Product(
                link=self.first_part_url + i["url"],
                name=i["name"].strip(),
                image=i["image"],
                price=float(re.sub(r'[ р.]', '', i["price"]).replace(',', '.')),
            )
            product_list.add_product(item)

        return product_list
