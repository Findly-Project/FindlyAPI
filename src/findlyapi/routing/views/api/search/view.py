import time
from typing import Callable

from fastapi.responses import JSONResponse

from findlyapi.schemas.search_payload import SearchPayload
from findlyapi.services.process_request.entity import ProcessRequest
from findlyapi.services.product_parser.models.product_models import ProductsListDTO, NamedProductsList


async def main_view_implementation(request_args: SearchPayload, request_metadata: Callable[[SearchPayload, float], dict]) -> JSONResponse:
    start_time: float = time.time()

    products: list[NamedProductsList] = await ProcessRequest(request_args).get_response()
    serialized_products: dict = ProductsListDTO(*products)()

    request_metadata: dict = request_metadata(request_args.model_dump(), round(time.time() - start_time, 4))

    content: dict[str, dict] = {
        "products_data": serialized_products,
        "request_metadata": request_metadata,
    }

    res: JSONResponse = JSONResponse(content, 200)
    res.headers["Content-Type"] = "application/json"

    return res