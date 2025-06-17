from datetime import datetime
from fastapi import Request

from src.schemas.search_payload import SearchPayload


def get_request_metadata(request: Request, request_args: SearchPayload) -> dict:
    request_metadata = {
        "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
        "request_args": request_args.model_dump(),
        "request_url": request.url.path,
        "response_code": 200,
    }

    return request_metadata