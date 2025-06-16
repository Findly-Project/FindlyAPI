import json
from httpx import Response

from src.services.product_parser.dto.base_from_dto import BaseFromDTO
from src.services.product_parser.models.product_models import ProductsList, Product


class FromOnlinerDTO(BaseFromDTO):
    def __init__(self, pars_data: Response):
        self.pars_data: str = pars_data.text

    def __call__(self) -> ProductsList:
        product_list: ProductsList = ProductsList()
        data: dict = json.loads(self.pars_data)

        for i in data["products"]:
            if i["prices"]:
                item: Product = Product(
                    link=i["html_url"],
                    name=i["full_name"].strip(),
                    image=i["images"]["header"],
                    price=float(i["prices"]["price_min"]["amount"]),
                )
                product_list.add_product(item)

        return product_list
