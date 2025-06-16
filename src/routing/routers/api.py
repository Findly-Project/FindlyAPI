from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.routing.views.api.search.view import main_view_implementation
from src.schemas.search_payload import SearchPayload


api_router = APIRouter(prefix="/api")

@api_router.post("/search")
async def main_view(request: Request, request_args: SearchPayload) -> JSONResponse:
    return await main_view_implementation(request_url=request.url.path,
                                          request_args=request_args,)
