from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from httpx import ConnectTimeout, ConnectError

from src.routing.exception_handlers import HTTPErrorHandlers
from src.routing.routers.api import api_router


app: FastAPI = FastAPI(title=__name__)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware, # type: ignore
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
