__all__ = (
    "configure_app",
    "create_app",
    "create_async_ioc_container",
)
from collections.abc import Iterable
from dishka import AsyncContainer, Provider, make_async_container
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from httpx import ConnectError, ConnectTimeout

from findlyapi.routing.exception_handlers import HTTPErrorHandlers
from findlyapi.routing.routers.api import api_router


def create_app() -> FastAPI:
    return FastAPI(title=__name__, default_response_class=ORJSONResponse)


def configure_app(app: FastAPI) -> None:
    app.include_router(api_router)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["*"]
    )

    app.exception_handler(RequestValidationError)(HTTPErrorHandlers.unprocessable_content_view)
    app.exception_handler(ConnectTimeout)(HTTPErrorHandlers.pars_timeout_view)
    app.exception_handler(ConnectError)(HTTPErrorHandlers.connect_error_view)
    app.exception_handler(404)(HTTPErrorHandlers.notfound_view)
    app.exception_handler(405)(HTTPErrorHandlers.method_not_allowed_view)


def create_async_ioc_container(providers: Iterable[Provider]) -> AsyncContainer:
    return make_async_container(*providers)