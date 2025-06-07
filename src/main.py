import time
from datetime import datetime

from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.request_args_middleware import RequestArgsMiddleware, CheckArgsEnum
from src.error_handlers import HTTPErrorHandlers
from src.services.collecting_primary_data.product_models import MarketPlaceList
from src.services.output_of_results import output_of_results
from src.models import RequestArgs

app: FastAPI = FastAPI(title=__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"]
)

api_router = APIRouter(prefix="/api")


@api_router.get("/search")
async def main_view(request: Request, args: RequestArgs = Depends()) -> JSONResponse:
    start_collect_data: float = time.time()
    args: RequestArgsMiddleware = RequestArgsMiddleware(args.model_dump())
    is_all_args_are_allowed: bool = args.checking_allowed_request_args()
    is_all_args_are_compatible: bool = args.checking_overlapping_arguments()

    if not is_all_args_are_allowed:
        raise HTTPException(422)

    if not is_all_args_are_compatible:
        raise HTTPException(422)

    max_size: int | CheckArgsEnum | False = args.checking_max_size_arg()
    only_new: CheckArgsEnum | False = args.checking_only_new_arg()
    enable_filter_by_price: CheckArgsEnum | False = (
        args.checking_enable_filter_by_price_arg()
    )
    enable_filter_by_name: CheckArgsEnum | False = (
        args.checking_enable_filter_by_name_arg()
    )
    query: str | False = args.checking_query_arg()
    exclusion_words: str | True = args.checking_exclusion_words_arg()

    clear_args: list[bool] = [
        max_size,
        only_new,
        query,
        enable_filter_by_price,
        enable_filter_by_name,
        exclusion_words,
    ]

    if not all(clear_args):
        raise HTTPException(422)

    if isinstance(max_size, CheckArgsEnum):
        max_size: int = max_size.value
    if isinstance(only_new, CheckArgsEnum):
        only_new: bool = only_new.value
    if isinstance(enable_filter_by_price, CheckArgsEnum):
        enable_filter_by_price: bool = enable_filter_by_price.value
    if isinstance(enable_filter_by_name, CheckArgsEnum):
        enable_filter_by_name: bool = enable_filter_by_name.value

    kwargs: dict[str, str | bool | int] = {
        "query": query,
        "max_size": max_size,
        "only_new": only_new,
        "enable_filter_by_price": enable_filter_by_price,
        "enable_filter_by_name": enable_filter_by_name,
        "exclusion_words": exclusion_words,
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
        "request_args": {
            "max_size": max_size,
            "only_new": only_new,
            "query": query,
            "enable_filter_by_price": enable_filter_by_price,
            "enable_filter_by_name": enable_filter_by_name,
            "exclusion_word": exclusion_words
            if isinstance(exclusion_words, list) else None,
        },
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

app.exception_handler(422)(HTTPErrorHandlers.unprocessable_content_view)
app.exception_handler(404)(HTTPErrorHandlers.notfound_view)
app.exception_handler(405)(HTTPErrorHandlers.method_not_allowed_view)
