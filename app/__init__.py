from fastapi import FastAPI

from app.driver import driver_init
from app.routes import router as find_by_link_routes


def get_app() -> FastAPI:
    driver_init()
    app = FastAPI()
    app.include_router(find_by_link_routes)
    return app
