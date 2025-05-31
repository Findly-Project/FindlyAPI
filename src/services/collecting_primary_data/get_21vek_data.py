from types import NoneType
import httpx
from httpx import Response
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from .product_models import ProductList, ProductData
from src.utils.get_config.get_pars_config import GetParsConfig


async def get_21vek_data(query: str) -> ProductList:
    _21vek_pars_config: dict = GetParsConfig.get_21vek_pars_config()

    query: str = query.strip()
    url: str = _21vek_pars_config["main_api_url"].format(query=query)

    async with httpx.AsyncClient(timeout=10.0) as client:
        data: Response = await client.get(url)

    soup: BeautifulSoup = BeautifulSoup(data.text, "html.parser")
    data: ResultSet = soup.find_all("li", class_="g-box_lseparator")

    product_list: ProductList = ProductList()

    for i in data:
        price: Tag = i.find("span", class_="j-item-data")
        if not isinstance(price, NoneType):
            price: str = price.text.rstrip("0").replace(r",", ".")
            price: float = float(price.replace(r" ", ""))

            item: ProductData = ProductData(
                link=i.find("a", class_="j-ga_track")["href"],
                name=i.find("span", class_="result__name").text.strip(),
                image=i.find("span", class_="result__img__inner").img["src"],
                price=price,
            )

            product_list.add_product(item)

    return product_list
