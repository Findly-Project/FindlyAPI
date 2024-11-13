from typing import Dict, Any
import httpx
from httpx import Response
import json
import logging
from utils.get_config.get_pars_config import GetParsConfig
from .product_models import ProductData, ProductList


async def get_kufar_data(query: str, only_new: bool) -> ProductList:
    kufar_pars_config: Dict = GetParsConfig.get_kufar_pars_config()

    query: str = query.strip()
    if only_new:
        url: str = kufar_pars_config["pars_url_only_new"].format(query=query)
    else:
        url: str = kufar_pars_config["pars_url_any"].format(query=query)
    first_part_image_url: str = kufar_pars_config["first_part_image_url"]

    async with httpx.AsyncClient(timeout=10.0) as client:
        data: Response = await client.get(url)

    data: Dict[Any] = json.loads(data.text)
    product_list: ProductList = ProductList()

    for i in data["ads"]:
        if i["images"]:
            try:
                item: ProductData = ProductData(
                    link=i["ad_link"],
                    name=i["subject"].strip(),
                    image=first_part_image_url + i["images"][0]["path"],
                    price=int(i["price_byn"]) / 100,
                )
                if int(i["price_byn"]):
                    product_list.add_product(item)

            except KeyError:
                item: ProductData = ProductData(
                    link=i["ad_link"],
                    name=i["subject"].strip(),
                    image=first_part_image_url + i["images"][1]["path"],
                    price=int(i["price_byn"]) / 100,
                )
                if int(i["price_byn"]):
                    product_list.add_product(item)

            except Exception as e:
                logging.error(e)

        else:
            item: ProductData = ProductData(
                link=i["ad_link"],
                name=i["subject"].strip(),
                price=int(i["price_byn"]) / 100,
            )
            if int(i["price_byn"]):
                product_list.add_product(item)

    return product_list
