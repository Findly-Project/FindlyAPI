from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.routing.views.api.search.view import main_view_implementation
from src.routing.views.api.search.depends import get_request_metadata
from src.schemas.search_payload import SearchPayload


api_router = APIRouter(prefix="/api")

@api_router.post("/search")
async def main_view(request_args: SearchPayload, request_metadata = Depends(get_request_metadata)) -> JSONResponse:
    return await main_view_implementation(request_args=request_args,
                                          request_metadata=request_metadata)
