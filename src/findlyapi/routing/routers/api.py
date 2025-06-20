from typing import Callable

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from findlyapi.routing.views.api.search.view import main_view_implementation
from findlyapi.schemas.search_payload import SearchPayload

api_router = APIRouter(prefix="/api", route_class=DishkaRoute)

@api_router.post("/search")
async def main_view(request_args: SearchPayload, request_metadata: FromDishka[Callable[[SearchPayload, float], dict]]) -> JSONResponse:
    return await main_view_implementation(request_args=request_args, request_metadata=request_metadata)
