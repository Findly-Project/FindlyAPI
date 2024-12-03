from typing import Dict, List
from utils.get_config.get_quart_config import GetQuartConfig


async def reject_middleware(ip: str):
    quart_security: Dict = GetQuartConfig.quart_security()
    allowed_ips: List = list(quart_security["allowed_ips"])

    if ip in allowed_ips:
        return True
    else:
        return False
