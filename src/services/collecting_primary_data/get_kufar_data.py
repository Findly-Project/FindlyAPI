import httpx
from httpx import Response
import json
from src.utils.get_config import GetParsConfig
from .product_models import ProductData, ProductList


async def get_kufar_data(query: str, only_new: bool) -> ProductList:
    kufar_pars_config: dict = GetParsConfig.get_kufar_pars_config()

    query: str = query.strip()
    if only_new:
        url: str = kufar_pars_config["pars_url_only_new"].format(query=query)
    else:
        url: str = kufar_pars_config["pars_url_any"].format(query=query)
    first_part_image_url: str = kufar_pars_config["first_part_image_url"]

    async with httpx.AsyncClient(timeout=20.0) as client:
        data: Response = await client.get(url)

    data: dict = json.loads(data.text)
    product_list: ProductList = ProductList()

    for i in data["ads"]:
        if i["images"]:
            if i["images"][0].get("path"):
                second_part_image_url: str = i["images"][0]["path"]
            else:
                second_part_image_url: str = i["images"][1]["path"]

            item: ProductData = ProductData(
                link=i["ad_link"],
                name=i["subject"].strip(),
                image=first_part_image_url + second_part_image_url,
                price=int(i["price_byn"]) / 100,
            )
            if int(i["price_byn"]):
                product_list.add_product(item)

        else:
            item: ProductData = ProductData(
                link=i["ad_link"],
                name=i["subject"].strip(),
                price=int(i["price_byn"]) / 100,
            )
            if int(i["price_byn"]):
                product_list.add_product(item)
    return product_list
