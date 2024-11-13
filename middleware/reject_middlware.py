from typing import Dict, List
from utils.get_config.get_quart_config import GetQuartConfig
from quart import Request


async def reject_middleware(request: Request):
    quart_security: Dict = GetQuartConfig.quart_security()
    allowed_ips: List = list(quart_security["allowed_ips"])

    if request.remote_addr in allowed_ips:
        return True
    else:
        return False
