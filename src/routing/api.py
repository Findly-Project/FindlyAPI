import time
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.schemas.search_payload import SearchPayload
from src.services.product_parser.models.product_models import MarketPlaceList
from src.services.output_of_results import output_of_results


api_router = APIRouter(prefix="/api")


@api_router.post("/search")
async def main_view(request: Request, request_args: SearchPayload) -> JSONResponse:
    start_collect_data: float = time.time()

    kwargs: dict[str, str | bool | int] = {
        "query": request_args.query,
        "max_size": request_args.max_size,
        "only_new": request_args.filters.only_new,
        "price_filter": request_args.filters.price_filter,
        "name_filter": request_args.filters.name_filter,
        "exclude_words": request_args.filters.exclude_words,
    }
    data: MarketPlaceList = await output_of_results(**kwargs)

    products_data: dict = data.get_json()
    request_metadata = {
        "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
        "response_time": round(time.time() - start_collect_data, 3),
        "size_of_products": {
            "all": sum([len(products_data[x]) for x in products_data]),
            "mmg": len(products_data.get("MMG", [])),
            "onliner": len(products_data.get("Onliner", [])),
            "kufar": len(products_data.get("Kufar", [])),
            "21vek": len(products_data.get("21vek", [])),
        },
        "request_args": kwargs,
        "request_url": request.url.path,
        "response_code": 200,
    }

    content: dict[str, dict] = {
        "products_data": products_data,
        "request_metadata": request_metadata,
    }
    res: JSONResponse = JSONResponse(content, 200)
    res.headers["Content-Type"] = "application/json"

    return res