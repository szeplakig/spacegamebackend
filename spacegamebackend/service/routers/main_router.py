from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from spacegamebackend.service.routers.research_router import create_research_router
from spacegamebackend.service.routers.structures_router import create_structures_router
from spacegamebackend.service.routers.system_router import create_system_router
from spacegamebackend.service.routers.user_resources_router import (
    create_user_resources_router,
)
from spacegamebackend.service.routers.user_router import create_user_router

origins = [
    "http://localhost:3000",
]


def create_main_router() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(create_user_router())

    app.include_router(create_system_router())

    app.include_router(create_structures_router())

    app.include_router(create_user_resources_router())

    app.include_router(create_research_router())

    return app
