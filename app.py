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
    is_allowed: bool = await reject_middleware(request)
    if is_allowed:

        args: RequestArgsMiddleware = RequestArgsMiddleware(request.args)
        is_all_args_are_allowed = args.check_allowed_request_args()

        if not is_all_args_are_allowed:
            abort(422)

        max_size: int | None = args.check_max_size_arg()
        only_new: bool | None = args.check_only_new_arg()
        query: str | False = args.check_query_arg()

        try:
            data: MarketPlaceList = await output_of_results(
                query=query, max_size=max_size, only_new=only_new
            )
        except (ConnectTimeout, ReadTimeout):
            data: MarketPlaceList = await output_of_results(
                query=query, max_size=max_size, only_new=only_new
            )
        json_data: Dict = data.get_json()
        content = {"data": json_data}

        res = await make_response(content, 200)

        if request.url.startswith(f"{HOST}:{PORT}/api/search"):
            res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Content-Type"] = "application/json"
        return res
    else:
        await abort(403)


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
