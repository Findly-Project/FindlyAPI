from types import NoneType
from typing import Dict
from httpx import ReadTimeout, ConnectTimeout
from quart import Quart, render_template, request, abort
from quart.helpers import make_response
from quart.wrappers import Response
from get_products_data.collecting_primary_data.product_models import MarketPlaceList
from get_products_data.output_of_results import output_of_results
import logging
from utils.get_config.get_quart_config import GetQuartConfig
from middleware.reject_middlware import reject_middleware


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
        allowed_args = {'q',
                        'max_size',
                        'only_new'}

        q = request.args.get('q')
        if not q:
            abort(422)
        max_size = request.args.get('max_size')
        only_new = request.args.get('only_new')
        if not isinstance(max_size, NoneType):
            try:
                map(int, max_size)
                if not (0 <= int(max_size) <= 21): raise ValueError
            except ValueError:
                abort(422)
        if only_new not in [None, NoneType, '0', '1']: abort(422)

        all_args = set(request.args.keys())
        if len(all_args - allowed_args) > 0:
            abort(422)
        query: str = request.args.get('q').replace("+", " ")

        try:
            data: MarketPlaceList = await output_of_results(query=query,
                                                            max_size=max_size,
                                                            only_new=only_new)
        except (ConnectTimeout, ReadTimeout):
            data: MarketPlaceList = await output_of_results(query=query,
                                                            max_size=max_size,
                                                            only_new=only_new)

        json_data: Dict = data.get_json()
        content = {"data": json_data}

        res = await make_response(content)

        if request.url.startswith('http://127.0.0.1:5000/api/search'):
            res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Content-Type'] = 'application/json'
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

    logging.warning("Start Findly...")
    print("\n\033[1m\033[30m\033[44m {} \033[0m".format("Start Findly..."))

    app.run(debug=DEBUG, host=HOST, port=PORT)
