from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from datetime import datetime
from httpx import ConnectTimeout, ConnectError


class HTTPErrorHandlers:
    @staticmethod
    def notfound_view(request: Request, exc: HTTPException) -> JSONResponse:
        content: dict = {
            "response_code": 404,
            "default_error": exc.detail,
            "pretty_error": "Page not found, check the path is correct",
            "request_metadata": {
                "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "request_url": request.url.path,
            },
        }
        res: JSONResponse = JSONResponse(content, 404)
        return res

    @staticmethod
    def method_not_allowed_view(request: Request, exc: HTTPException) -> JSONResponse:
        content: dict = {
            "response_code": 405,
            "default_error": exc.detail,
            "pretty_error": "Request method not allowed",
            "request_metadata": {
                "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "request_url": request.url.path,
            },
        }
        res: JSONResponse = JSONResponse(content, 405)
        return res

    @staticmethod
    def unprocessable_content_view(request: Request, exc: RequestValidationError) -> Response:
        errors = exc.errors()
        custom_messages = []
        default_errors = []
        for error in errors:
            if error in default_errors:
                continue

            field_name = error['loc'][-1]
            if error['type'] == 'missing':
                custom_messages.append({"error_type": "missing",
                                        "error": {
                                            "error_field": field_name,
                                            "error_msg": "Missing required field"}
                                        })
            else:
                custom_messages.append({"error_type": "validation",
                                        "error": {
                                            "error_field": field_name,
                                            "error_msg": error['msg']}
                                        })
            default_errors.append(error)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({
                "response_code": 422,
                "pretty_error": "Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md",
                "specific_error": custom_messages,
                "request_metadata": {
                    "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                    "request_url": request.url.path,
                },

            })
        )

    @staticmethod
    def pars_timeout_view(request: Request, exc: ConnectTimeout) -> JSONResponse:
        content: dict = {
            "response_code": 504,
            "pretty_error": "Handle timeout exception when parse. Please try again later",
            "request_metadata": {
                "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "request_url": request.url.path,
            },
        }
        res: JSONResponse = JSONResponse(content, 504)
        return res

    @staticmethod
    def connect_error_view(request: Request, exc: ConnectError) -> JSONResponse:
        content: dict = {
            "response_code": 503,
            "pretty_error": "The server has no internet connection. Please try again later",
            "request_metadata": {
                "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "request_url": request.url.path,
            },
        }
        res: JSONResponse = JSONResponse(content, 503)
        return res
