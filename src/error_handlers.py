from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, Response

from datetime import datetime


class HTTPErrorHandlers:
    @staticmethod
    async def notfound_view(request: Request, exc: HTTPException) -> JSONResponse:
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
    async def method_not_allowed_view(request: Request, exc: HTTPException) -> JSONResponse:
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
    def unprocessable_content_view(request: Request, exc: HTTPException) -> Response:
        content: dict = {
            "response_code": 422,
            "default_error": exc.detail,
            "pretty_error": "Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md",
            "request_metadata": {
                "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "request_url": request.url.path,
            },
        }
        res: JSONResponse = JSONResponse(content, 422)
        return res