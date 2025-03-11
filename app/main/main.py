import asyncio
from contextlib import asynccontextmanager
import os
import logging
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.settings import get_settings, Settings
from starlette.middleware.cors import CORSMiddleware


settings: Settings = get_settings()





def create_app() -> CORSMiddleware:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI(
        title=settings.PROJECT_NAME + " API",
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )


    os.makedirs("media/category", exist_ok=True)
    os.makedirs("media/profile_picture", exist_ok=True)
    os.makedirs("media/product_image", exist_ok=True)
    os.makedirs("media/rating", exist_ok=True)
    app.mount("/media", StaticFiles(directory="media"), name="media")

    v1_router = APIRouter(prefix=settings.API_V1_STR)


    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


