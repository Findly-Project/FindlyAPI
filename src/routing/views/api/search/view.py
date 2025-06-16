import time
from fastapi.responses import JSONResponse

from .depends import get_request_metadata
from src.schemas.search_payload import SearchPayload
from src.services.process_request.entity import ProcessRequest
from src.services.product_parser.models.product_models import ProductsListDTO, NamedProductsList


async def main_view_implementation(request_url: str, request_args: SearchPayload) -> JSONResponse:
    start_time: float = time.time()

    products: list[NamedProductsList] = await ProcessRequest(request_args).get_response()
    serialized_products: dict = ProductsListDTO(*products)()

    request_metadata = get_request_metadata(start_time=start_time,
                                            products_data=serialized_products,
                                            request_args=request_args,
                                            request_url=request_url)

    content: dict[str, dict] = {
        "products_data": serialized_products,
        "request_metadata": request_metadata,
    }

    res: JSONResponse = JSONResponse(content, 200)
    res.headers["Content-Type"] = "application/json"

    return res