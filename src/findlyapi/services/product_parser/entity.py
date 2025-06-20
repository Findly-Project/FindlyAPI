import httpx
from httpx import Response

from findlyapi.services.product_parser.dto.from_21vek_dto import From21vekDTO
from findlyapi.services.product_parser.dto.from_kufar_dto import FromKufarDTO
from findlyapi.services.product_parser.dto.from_mmg_data import FromMmgDTO
from findlyapi.services.product_parser.dto.from_onliner_dto import FromOnlinerDTO
from findlyapi.services.product_parser.models.product_models import ProductsList
from findlyapi.utils.get_config import GetParsConfig


class ProductParser:
    def __init__(self, query: str):
        self.query = query.strip()

    async def get_21vek_data(self) -> ProductsList:
        _21vek_pars_config: dict = GetParsConfig.get_21vek_pars_config()
        url: str = _21vek_pars_config["main_api_url"].format(query=self.query)
        first_part_url: str = _21vek_pars_config["first_part_url"]
        async with httpx.AsyncClient(timeout=10.0) as client:
            data: Response = await client.get(url)

        return From21vekDTO(data, first_part_url)()

    async def get_kufar_data(self, only_new: bool) -> ProductsList:
        kufar_pars_config: dict = GetParsConfig.get_kufar_pars_config()
        if only_new:
            url: str = kufar_pars_config["pars_url_only_new"].format(query=self.query)
        else:
            url: str = kufar_pars_config["pars_url_any"].format(query=self.query)
        first_part_image_url: str = kufar_pars_config["first_part_image_url"]

        async with httpx.AsyncClient(timeout=20.0) as client:
            data: Response = await client.get(url)

        return FromKufarDTO(data, first_part_image_url)()

    async def get_mmg_data(self) -> ProductsList:
        mmg_pars_config: dict = GetParsConfig.get_mmg_pars_config()

        query: str = self.query.replace(" ", "+")
        first_part_url: str = mmg_pars_config["first_part_url"]
        first_part_image_url: str = mmg_pars_config["first_part_image_url"]
        url: str = mmg_pars_config["main_pars_url"].format(query=query)

        async with httpx.AsyncClient(timeout=10.0) as client:
            data: Response = await client.get(url)

        return FromMmgDTO(data, first_part_url, first_part_image_url)()

    async def get_onliner_data(self) -> ProductsList:
        onliner_pars_data: dict = GetParsConfig.get_onliner_pars_config()
        query: str = self.query.replace(" ", "+")

        url: str = onliner_pars_data["main_api_url"].format(query=query, page=1)

        async with httpx.AsyncClient(timeout=10.0) as client:
            data: Response = await client.get(url)

        return FromOnlinerDTO(data)()


