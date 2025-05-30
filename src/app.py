from datetime import datetime
import time
from services.collecting_primary_data.product_models import MarketPlaceList
from services.output_of_results import output_of_results
import logging
from utils.get_config.get_quart_config import GetQuartConfig
from middleware.request_args_middleware import (
    RequestArgsMiddleware,
    CheckArgsEnum
)

from fastapi import FastAPI, APIRouter


app: FastAPI =FastAPI(title=__name__)
config: dict = GetQuartConfig.quart_settings()

DEBUG: bool = bool(int(config["DEBUG"]))
HOST: str = config["HOST"]
PORT: int = int(config["PORT"])


@app.exception_handler(404)
async def notfound_view(error) -> Response:
    content: Response = jsonify({'response_code': 404,
                       'default_error': str(error),
                       'pretty_error': 'Page not found, check the path is correct',
                       'request_metadata': {
                           'date': datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                           'request_url': request.url}
                       })
    res: Response = await make_response(content, 404)
    return res


@app.exception_handler(405)
async def method_not_allowed_view(error) -> Response:
    content: Response = jsonify({'response_code': 405,
                       'default_error': str(error),
                       'pretty_error': 'Request method not allowed',
                       'request_metadata': {
                           'date': datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                           'request_url': request.url}
                       })
    res: Response = await make_response(content, 405)
    return res


@app.exception_handler(403)
async def unauthorized_view(error) -> Response:
    content: Response = jsonify({'response_code': 403,
                       'default_error': str(error),
                       'pretty_error': 'Access to API is denied',
                       'request_metadata': {
                           'date': datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                           'request_url': request.url}
                       })
    res: Response = await make_response(content, 403)
    return res


@app.exception_handler(422)
async def unprocessable_content_view(error) -> Response:
    content: Response = jsonify({'response_code': 422,
                       'default_error': str(error),
                       'pretty_error': 'Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md',
                       'request_metadata': {
                            'date': datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                            'request_url': request.url}
                       })
    res: Response = await make_response(content, 422)
    return res


api_router = APIRouter(prefix="/api")

@app.get("/api/search")
async def main_view() -> Response | str:
    start_collect_data: float = time.time()
    args: RequestArgsMiddleware = RequestArgsMiddleware(request.args)
    is_all_args_are_allowed: bool = args.checking_allowed_request_args()
    is_all_args_are_compatible: bool = args.checking_overlapping_arguments()

    if not is_all_args_are_allowed:
        await abort(422)

    if not is_all_args_are_compatible:
        await abort(422)

    max_size: int | CheckArgsEnum | False = args.checking_max_size_arg()
    only_new: CheckArgsEnum | False = args.checking_only_new_arg()
    enable_filter_by_price: CheckArgsEnum | False = args.checking_enable_filter_by_price_arg()
    enable_filter_by_name: CheckArgsEnum | False = args.checking_enable_filter_by_name_arg()
    query: str | False = args.checking_query_arg()
    exclusion_words: str | True = args.checking_exclusion_words_arg()

    clear_args: list[bool] = [max_size, only_new, query, enable_filter_by_price, enable_filter_by_name, exclusion_words]

    if not all(clear_args):
        await abort(422)

    if isinstance(max_size, CheckArgsEnum):
        max_size: int = max_size.value
    if isinstance(only_new, CheckArgsEnum):
        only_new: bool = only_new.value
    if isinstance(enable_filter_by_price, CheckArgsEnum):
        enable_filter_by_price: bool = enable_filter_by_price.value
    if isinstance(enable_filter_by_name, CheckArgsEnum):
        enable_filter_by_name: bool = enable_filter_by_name.value

    kwargs: dict[str, str | bool | int] = {
        'query': query,
        'max_size': max_size,
        'only_new': only_new,
        'enable_filter_by_price': enable_filter_by_price,
        'enable_filter_by_name': enable_filter_by_name,
        'exclusion_words': exclusion_words
    }
    data: MarketPlaceList = await output_of_results(
        **kwargs
    )

    products_data: dict = data.get_json()
    request_metadata = {'date': datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                        'response_time': round(time.time() - start_collect_data, 3),
                        'size_of_products':{
                            'all': sum([len(products_data[x]) for x in products_data]),
                            'mmg': len(products_data.get('MMG') if products_data.get('MMG') else []),
                            'onliner': len(products_data.get('Onliner') if products_data.get('Onliner') else []),
                            'kufar': len(products_data.get('Kufar') if products_data.get('Kufar') else []),
                            '21vek': len(products_data.get('21vek') if products_data.get('21vek') else [])
                        },
                        'request_args':{
                            'max_size': max_size,
                            'only_new': only_new,
                            'query': query,
                            'enable_filter_by_price': enable_filter_by_price,
                            'enable_filter_by_name': enable_filter_by_name,
                            'exclusion_word': exclusion_words if isinstance(exclusion_words, list) else None
                        },
                        'request_url': request.url,
                        'response_code': 200}

    content: dict[str, dict] = {"products_data": products_data,
                                "request_metadata": request_metadata}

    res: Response = await make_response(content, 200)

    if request.url.startswith(f"{HOST}:{PORT}/api/search"):
        res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res



logging.basicConfig(
    level=logging.WARNING,
    filename="secret_data/logs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n\n",
)

app.include_router(api_router)
