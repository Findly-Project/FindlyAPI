from datetime import datetime
from typing import Callable

from fastapi import Request
from dishka import Provider, provide, Scope

from findlyapi.schemas.search_payload import SearchPayload


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_request_metadata(self, request: Request) -> Callable[[SearchPayload, float], dict]:
        metadata = lambda payload, response_time: {
            "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
            "request_args": payload,
            "response_time": response_time,
            "request_url": str(request.url),
            "response_code": 200,
        }

        return metadata
