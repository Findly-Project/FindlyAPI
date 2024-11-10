import tomllib
from typing import Dict


class GetQuartConfig:
    @staticmethod
    def quart_settings() -> Dict:
        with open("backend/secret_data/config.toml", "rb") as config:
            quart_settings: Dict[str] = tomllib.load(config)["Quart"]["Settings"]

        return quart_settings

    @staticmethod
    def quart_security() -> Dict:
        with open("backend/secret_data/config.toml", "rb") as config:
            quart_security: Dict[str] = tomllib.load(config)["Quart"]["Security"]

        return quart_security
