import json
from httpx import Response

from src.services.product_parser.dto.base_from_dto import BaseFromDTO
from src.services.product_parser.models.product_models import ProductsList, Product


class FromMmgDTO(BaseFromDTO):
    def __init__(self, pars_data: Response, first_part_url: str, first_part_image_url: str):
        self.pars_data: str = pars_data.text
        self.first_part_url: str = first_part_url
        self.first_part_image_url: str = first_part_image_url

    def __call__(self) -> ProductsList:
        product_list: ProductsList = ProductsList()
        data: dict = json.loads(self.pars_data)

        for i in data.get('items', []):
            item: Product = Product(
                link=self.first_part_url + i["id"],
                name=i["name"].strip(),
                image=self.first_part_image_url + i["img"],
                price=float(i["cost"].replace(',', '.')),
            )
            product_list.add_product(item)

        return product_list
