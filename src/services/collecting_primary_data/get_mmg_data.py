import httpx
from httpx import Response
from bs4 import BeautifulSoup
import logging
from src.utils.get_config import GetParsConfig
from .product_models import ProductData, ProductList
import re


async def get_mmg_data(query: str) -> ProductList:
    mmg_pars_config: dict = GetParsConfig.get_mmg_pars_config()

    query: str = query.strip().replace(" ", "+")
    first_part_url: str = mmg_pars_config["first_part_url"]
    url: str = mmg_pars_config["main_pars_url"].format(query=query)

    async with httpx.AsyncClient(timeout=10.0) as client:
        data: Response = await client.get(url)

    soup: BeautifulSoup = BeautifulSoup(data.text, "html.parser")
    data_soup: list = soup.find_all("div", class_="item")

    product_list: ProductList = ProductList()

    for i in data_soup:
        try:
            price: str = i.find("span", class_="price").text
            price: float = float(re.sub(r"[^\d.]", "", price).rstrip("."))

            item: ProductData = ProductData(
                link=first_part_url + i.find("a", class_="title")["href"],
                name=i.find("a", class_="title").text.strip(),
                image=first_part_url + i.find("div", class_="listener").img["src"],
                price=price,
            )
        except (TypeError, AttributeError):
            continue
        except Exception as e:
            logging.error(e)
        else:
            product_list.add_product(item)

    return product_list
