from datetime import datetime
import time
from typing import Dict
from httpx import ReadTimeout, ConnectTimeout
from quart import Quart, render_template, request, abort
from quart.helpers import make_response
from quart.wrappers import Response
from services.collecting_primary_data.product_models import MarketPlaceList
from services.output_of_results import output_of_results
import logging
from utils.get_config.get_quart_config import GetQuartConfig
from middleware.reject_middleware import reject_middleware
from middleware.request_args_middleware import (
    RequestArgsMiddleware,
    CheckArgsEnum
)


app: Quart = Quart(__name__)
config: Dict = GetQuartConfig.quart_settings()

DEBUG: bool = bool(int(config["DEBUG"]))
HOST: str = config["HOST"]
PORT: int = int(config["PORT"])


@app.errorhandler(404)
async def notfound_view(error) -> Response:
    content = await render_template("notfound_page.html")
    res = await make_response(content, 404)
    return res


@app.errorhandler(405)
async def method_not_allowed_view(error) -> Response:
    content = await render_template("method_not_allowed_page.html")
    res = await make_response(content, 405)
    return res


@app.errorhandler(403)
async def unauthorized_view(error) -> Response:
    content = await render_template("unauthorized_page.html")
    res = await make_response(content, 403)
    return res


@app.errorhandler(422)
async def unprocessable_content_view(error) -> Response:
    content = await render_template("unprocessable_content_page.html")
    res = await make_response(content, 422)
    return res


@app.route("/api/search", methods=["GET"])
async def main_view() -> Response | str:
    is_allowed: bool = await reject_middleware(request.remote_addr)
    if not is_allowed:
        await abort(403)

    start_collect_data = time.time()
    args: RequestArgsMiddleware = RequestArgsMiddleware(request.args)
    is_all_args_are_allowed = args.check_allowed_request_args()

    if not is_all_args_are_allowed:
        await abort(422)

    max_size: int | CheckArgsEnum | False = args.check_max_size_arg()
    only_new: CheckArgsEnum | False = args.check_only_new_arg()
    enable_filter_by_price: CheckArgsEnum | False = args.check_enable_filter_by_price_arg()
    enable_filter_by_name: CheckArgsEnum | False = args.check_enable_filter_by_name_arg()
    query: str | False = args.check_query_arg()
    exclusion_word: str | True = args.check_exclusion_word_arg()

    clear_args = [max_size, only_new, query, enable_filter_by_price, enable_filter_by_name, exclusion_word]

    if not all(clear_args):
        await abort(422)

    if isinstance(max_size, CheckArgsEnum):
        max_size = max_size.value
    if isinstance(only_new, CheckArgsEnum):
        only_new = only_new.value
    if isinstance(enable_filter_by_price, CheckArgsEnum):
        enable_filter_by_price = enable_filter_by_price.value
    if isinstance(enable_filter_by_name, CheckArgsEnum):
        enable_filter_by_name = enable_filter_by_name.value

    try:
        data: MarketPlaceList = await output_of_results(
            query=query,
            max_size=max_size,
            only_new=only_new,
            enable_filter_by_price=enable_filter_by_price,
            enable_filter_by_name = enable_filter_by_name,
            exclusion_word=exclusion_word
        )
    except (ConnectTimeout, ReadTimeout):
        data: MarketPlaceList = await output_of_results(
            query=query,
            max_size=max_size,
            only_new=only_new,
            enable_filter_by_price=enable_filter_by_price,
            enable_filter_by_name=enable_filter_by_name,
            exclusion_word=exclusion_word
        )
    products_data: Dict = data.get_json()
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
                            'exclusion_word': exclusion_word if isinstance(exclusion_word, str) else None
                        },
                        'request_url': request.url}

    content = {"products_data": products_data,
               "request_metadata": request_metadata}

    res = await make_response(content, 200)

    if request.url.startswith(f"{HOST}:{PORT}/api/search"):
        res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        filename="secret_data/logs.log",
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n\n",
    )

    logging.warning("Start FindlyAPI...")
    print("\n\033[1m\033[30m\033[44m {} \033[0m".format("Start FindlyAPI..."))

    app.run(debug=DEBUG, host=HOST, port=PORT)
