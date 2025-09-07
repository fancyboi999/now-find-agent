from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.providers import app_provider, exception_provider, logging_provider
from config.config import DevelopmentSettings, ProductionSettings, get_settings

settings = get_settings()


def register(app: FastAPI, provider, settings: DevelopmentSettings | ProductionSettings):
    provider.register(app, settings)


def boot(app: FastAPI, provider):
    provider.boot(app)


def create_app() -> FastAPI:
    """
    Storing object instances in the app context: https://github.com/fastapi/fastapi/issues/81

    Returns:
        FastAPI: _description_
    """

    app = FastAPI(lifespan=app_provider.lifespan)

    register(app, app_provider, settings)
    register(app, logging_provider, settings)
    register(app, exception_provider, settings)

    app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static",
    )

    return app
