import tomllib


class GetQuartConfig:
    @staticmethod
    def quart_settings() -> dict[str]:
        with open("secret_data/config.toml", "rb") as config:
            quart_settings: dict[str] = tomllib.load(config)["Quart"]["Settings"]

        return quart_settings

    @staticmethod
    def quart_security() -> dict[str]:
        with open("secret_data/config.toml", "rb") as config:
            quart_security: dict[str] = tomllib.load(config)["Quart"]["Security"]

        return quart_security
