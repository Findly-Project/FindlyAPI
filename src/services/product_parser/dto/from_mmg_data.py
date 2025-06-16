import re
from bs4 import BeautifulSoup
from httpx import Response

from src.services.product_parser.dto.base_from_dto import BaseFromDTO
from src.services.product_parser.models.product_models import ProductsList, Product


class FromMmgDTO(BaseFromDTO):
    def __init__(self, pars_data: Response, first_part_url: str):
        self.pars_data: str = pars_data.text
        self.first_part_url: str = first_part_url

    def __call__(self) -> ProductsList:
        soup: BeautifulSoup = BeautifulSoup(self.pars_data, "html.parser")
        data_soup: list = soup.find_all("div", class_="item")

        product_list: ProductsList = ProductsList()

        for i in data_soup:
            try:
                price: str = i.find("span", class_="price").text
                price: float = float(re.sub(r"[^\d.]", "", price).rstrip("."))

                item: Product = Product(
                    link=self.first_part_url + i.find("a", class_="title")["href"],
                    name=i.find("a", class_="title").text.strip(),
                    image=self.first_part_url + i.find("div", class_="listener").img["src"],
                    price=price,
                )
            except (TypeError, AttributeError):
                continue
            else:
                product_list.add_product(item)

        return product_list
