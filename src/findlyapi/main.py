from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
import uvicorn

from findlyapi.setup.app_factory import create_async_ioc_container, create_app, configure_app
from findlyapi.setup.ioc.registry import get_providers


def make_app() -> FastAPI:
    app: FastAPI = create_app()
    configure_app(app=app)
    async_ioc_container = create_async_ioc_container(
        providers=get_providers(),
    )
    setup_dishka(container=async_ioc_container, app=app)

    return app


if __name__ == "__main__":
    uvicorn.run(
        app=make_app(),
        port=8000,
        reload=False,
    )