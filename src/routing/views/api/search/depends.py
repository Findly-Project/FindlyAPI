import time
from datetime import datetime

from src.schemas.search_payload import SearchPayload


def get_request_metadata(start_time: float,
                         products_data: dict,
                         request_args: SearchPayload,
                         request_url: str) -> dict:

    request_metadata = {
        "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
        "response_time": round(time.time() - start_time, 3),
        "size_of_products": {
            "all": sum([len(products_data[x]) for x in products_data]),
            "mmg": len(products_data.get("MMG", [])),
            "onliner": len(products_data.get("Onliner", [])),
            "kufar": len(products_data.get("Kufar", [])),
            "21vek": len(products_data.get("21vek", [])),
        },
        "request_args": request_args.model_dump(),
        "request_url": request_url,
        "response_code": 200,
    }

    return request_metadata