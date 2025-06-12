import time
from datetime import datetime

from fastapi import FastAPI, APIRouter, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.error_handlers import HTTPErrorHandlers
from src.services.collecting_primary_data.product_models import MarketPlaceList
from src.services.output_of_results import output_of_results
from src.models import SearchPayload


app: FastAPI = FastAPI(title=__name__)

api_router = APIRouter(prefix="/api")


@api_router.get("/search")
async def main_view(request: Request, request_args: SearchPayload) -> JSONResponse:
    start_collect_data: float = time.time()

    kwargs: dict[str, str | bool | int] = {
        "query": request_args.query,
        "max_size": request_args.max_size,
        "only_new": request_args.filters.only_new,
        "enable_filter_by_price": request_args.filters.price_filter,
        "enable_filter_by_name": request_args.filters.name_filter,
        "exclusion_words": request_args.filters.exclude_words,
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


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware, # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"]
)

app.exception_handler(RequestValidationError)(HTTPErrorHandlers.unprocessable_content_view)
app.exception_handler(422)(HTTPErrorHandlers.unprocessable_content_view)
app.exception_handler(404)(HTTPErrorHandlers.notfound_view)
app.exception_handler(405)(HTTPErrorHandlers.method_not_allowed_view)
