from types import NoneType
from bs4 import Tag, ResultSet, BeautifulSoup
from httpx import Response

from src.services.product_parser.dto.base_from_dto import BaseFromDTO
from src.services.product_parser.models.product_models import ProductsList, Product


class From21vekDTO(BaseFromDTO):
    def __init__(self, pars_data: Response):
        self.pars_data: str = pars_data.text

    def __call__(self) -> ProductsList:
        soup: BeautifulSoup = BeautifulSoup(self.pars_data, "html.parser")
        data: ResultSet = soup.find_all("li", class_="g-box_lseparator")

        product_list: ProductsList = ProductsList()

        for i in data:
            price: Tag = i.find("span", class_="j-item-data")
            if not isinstance(price, NoneType):
                price: str = price.text.rstrip("0").replace(r",", ".")
                price: float = float(price.replace(r" ", ""))

                item: Product = Product(
                    link=i.find("a", class_="j-ga_track")["href"],
                    name=i.find("span", class_="result__name").text.strip(),
                    image=i.find("span", class_="result__img__inner").img["src"],
                    price=price,
                )

                product_list.add_product(item)

        return product_list
