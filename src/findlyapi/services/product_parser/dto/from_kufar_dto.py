import json
from httpx import Response

from findlyapi.services.product_parser.dto.base_from_dto import BaseFromDTO
from findlyapi.services.product_parser.models.product_models import ProductsList, Product


class FromKufarDTO(BaseFromDTO):
    def __init__(self, pars_data: Response, first_part_image_url: str):
        self.pars_data: str = pars_data.text
        self.first_part_image_url: str = first_part_image_url

    def __call__(self) -> ProductsList:
        data: dict = json.loads(self.pars_data)
        product_list: ProductsList = ProductsList()

        for i in data["ads"]:
            if i["images"]:
                if i["images"][0].get("path"):
                    second_part_image_url: str = i["images"][0]["path"]
                else:
                    second_part_image_url: str = i["images"][1]["path"]

                item: Product = Product(
                    link=i["ad_link"],
                    name=i["subject"].strip(),
                    image=self.first_part_image_url + second_part_image_url,
                    price=int(i["price_byn"]) / 100,
                )
                if int(i["price_byn"]):
                    product_list.add_product(item)

            else:
                item: Product = Product(
                    link=i["ad_link"],
                    name=i["subject"].strip(),
                    price=int(i["price_byn"]) / 100,
                )
                if int(i["price_byn"]):
                    product_list.add_product(item)
        return product_list
