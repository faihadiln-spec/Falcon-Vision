from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.auth_routes import router as auth_router
from app.api.routes.employee_face_routes import router as employee_face_router
from app.api.routes.employee_routes import router as employee_router
from app.api.routes.health_routes import router as health_router
from app.api.routes.user_routes import router as user_router
from app.core.config import get_settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.exceptions import AppError


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(employee_router, prefix="/api/employees", tags=["Employees"])
app.include_router(employee_face_router, prefix="/api/employee-faces", tags=["Employee Faces"])
