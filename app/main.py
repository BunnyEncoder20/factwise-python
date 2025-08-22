from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import users, teams, boards

app = FastAPI(title="Project Board API")

# Handle request validation errors (Pydantic + JSON parsing issues)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid request",
            "details": exc.errors(),  # you can trim this if too verbose
        },
    )

# Handle generic HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
        },
    )

# Catch-all for any unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),  # ⚠️ careful, maybe hide this in prod
        },
    )

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(boards.router)
