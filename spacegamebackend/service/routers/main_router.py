import time
from collections.abc import Callable
from datetime import timedelta

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from spacegamebackend.service.routers.system_router import create_system_router
from spacegamebackend.service.routers.user_router import create_user_router

origins = [
    "http://localhost:3000",
    # Add other origins if necessary
]


def create_main_router() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allows requests from listed origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # Allows all headers
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        print(f"Time took to process the request and return response is {timedelta(seconds=time.time() - start_time)}")
        response.headers["X-Process-Time"] = str(timedelta(seconds=time.time() - start_time))
        return response

    app.include_router(create_system_router())

    app.include_router(create_user_router())

    return app
