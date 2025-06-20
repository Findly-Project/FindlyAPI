from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
import uvicorn

from findlyapi.setup.app_factory import create_async_ioc_container, create_app, configure_app
from findlyapi.setup.ioc.registry import get_providers


app: FastAPI = create_app()

configure_app(app=app)
setup_dishka(container=create_async_ioc_container(providers=get_providers()), app=app)


if __name__ == "__main__":
    uvicorn.run(
        app="findlyapi.main:app",
        port=8000,
        reload=True,
    )