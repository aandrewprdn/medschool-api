from contextlib import asynccontextmanager

import loguru
import orjson
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from src.models.base_application_error import BaseApplicationException
from src.models.validaiton_error_data import PydanticValidationErrorData


@asynccontextmanager
async def lifespan(app: FastAPI): ...


def register_routers(app: FastAPI) -> None: ...


def register_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def error_handler_middleware(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            loguru.logger.error(
                f"Unhandled Exception: {str(exc)} | Path: {request.url}"
            )
            return JSONResponse(
                status_code=500,
                content={
                    "errors": [
                        {
                            "message": "Internal Server Error",
                            "detail": str(exc),
                        }
                    ]
                },
            )

    @app.middleware("http")
    async def log_request_headers(request: Request, call_next):
        loguru.logger.info(f"Raw Headers: {dict(request.headers)}")
        response = await call_next(request)
        return response

    @app.middleware("http")
    async def log_response_body_on_error(request: Request, call_next):
        response = await call_next(request)

        if request.method.lower() == "post" and response.status_code >= 400:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            loguru.logger.error(f"Error Response Body: {body.decode('utf-8')}")

            async def new_body_iterator():
                yield body

            response.body_iterator = new_body_iterator()
        return response

    @app.middleware("http")
    async def custom_404_middleware(request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "errors": [
                        {
                            "message": "Resource not found",
                            "detail": f"The requested resource does not exist: {request.url}",
                        }
                    ]
                },
            )
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        loguru.logger.error(f"HTTP Exception: {exc.detail} | Path: {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "errors": [
                    {
                        "message": "HTTP Exception",
                        "detail": str(exc.detail),
                    }
                ]
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_exception_handler(
        request: Request, exc: ValidationError
    ):
        data = PydanticValidationErrorData(**orjson.loads(exc.json())[0])
        message = f"Received invalid fields - {data.loc}"

        loguru.logger.error(f"Validation Exception: {message} | Path: {request.url}")
        return JSONResponse(
            status_code=422,
            content={
                "errors": [
                    {
                        "message": message,
                        "detail": {"msg": data.msg, "invalid_input": data.input},
                    }
                ]
            },
        )

    @app.exception_handler(BaseApplicationException)
    async def base_exception_handler(request: Request, exc: BaseApplicationException):
        loguru.logger.error(f"Base app Exception: {exc.message} | Path: {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "errors": [
                    {
                        "message": exc.message,
                        "detail": exc.details,
                    }
                ]
            },
        )


def create_app():
    app = FastAPI(
        debug=False,
        redoc_url=None,
        openapi_url="/api/ale/docs/openapi.json",
    )
    register_middlewares(app)
    register_exceptions_handlers(app)
    return app
