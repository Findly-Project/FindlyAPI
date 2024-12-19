from utils.get_config.get_quart_config import GetQuartConfig


async def reject_middleware(ip: str):
    quart_security: dict = GetQuartConfig.quart_security()
    allowed_ips: list = list(quart_security["allowed_ips"])

    if ip in allowed_ips:
        return True
    else:
        return False
