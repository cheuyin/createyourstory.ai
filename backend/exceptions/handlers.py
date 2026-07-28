from collections.abc import Callable

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.exceptions import (
    AuthenticationError,
    AuthorizationError,
    CreateYourStoryError,
    ImageGenerationException,
    InsufficientCreditsError,
    JobNotFoundError,
    StoryGenerationError,
    StoryNotFoundError,
    StoryResponseValidationError,
    StoryRootNotFoundError,
    UnsupportedAIModelError,
)

_DOMAIN_EXCEPTION_STATUS: list[
    tuple[type[CreateYourStoryError], int, dict[str, str] | None]
] = [
    (ImageGenerationException, status.HTTP_503_SERVICE_UNAVAILABLE, None),
    (InsufficientCreditsError, status.HTTP_402_PAYMENT_REQUIRED, None),
    (AuthenticationError, status.HTTP_401_UNAUTHORIZED,
     {"WWW-Authenticate": "Bearer"}),
    (AuthorizationError, status.HTTP_403_FORBIDDEN, None),
    (UnsupportedAIModelError, status.HTTP_400_BAD_REQUEST, None),
    (StoryGenerationError, status.HTTP_500_INTERNAL_SERVER_ERROR, None),
    (StoryResponseValidationError, status.HTTP_500_INTERNAL_SERVER_ERROR, None),
    (StoryRootNotFoundError, status.HTTP_500_INTERNAL_SERVER_ERROR, None),
    (StoryNotFoundError, status.HTTP_404_NOT_FOUND, None),
    (JobNotFoundError, status.HTTP_404_NOT_FOUND, None),
]


def _domain_error_response(
    exc: CreateYourStoryError,
    status_code: int,
    *,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": exc.name, "message": exc.message},
        headers=headers,
    )


def _make_domain_handler(
    status_code: int,
    headers: dict[str, str] | None = None,
) -> Callable[[Request, CreateYourStoryError], JSONResponse]:
    def handler(_: Request, exc: CreateYourStoryError) -> JSONResponse:
        return _domain_error_response(exc, status_code, headers=headers)

    return handler


def register_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code, headers in _DOMAIN_EXCEPTION_STATUS:
        app.add_exception_handler(
            exc_class, _make_domain_handler(status_code, headers))

    app.add_exception_handler(
        CreateYourStoryError,
        _make_domain_handler(status.HTTP_500_INTERNAL_SERVER_ERROR),
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Validation error",
                "message": "The request was poorly formatted",
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "message": "Something went wrong"},
        )
