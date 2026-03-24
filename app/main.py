from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException
from .common.database.firestore import init_db
from .common.middleware.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    api_exception_handler,
    APIException,
    ErrorCode
)
from fastapi.middleware.cors import CORSMiddleware
from .common.middleware.sanitizer_middleware import SanitizeNullMiddleware
from .common.middleware.logger import get_app_logger, LOGGING_CONFIG
from .auth.controller import router as auth_router
from .product.controller import router as product_router



# Configure logger
logger = get_app_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is starting...")
    init_db()
    logger.info("Firebase Firestore initialized successfully.")
    yield
    logger.info("App is shutting down...")

app = FastAPI(
    title="Thisai Courier API Store",
    description="API documentation for Thisai Courier App – managing shipments, tracking, delivery agents, and logistics.",
    version="1.0.0",
    lifespan=lifespan,
    log_config=LOGGING_CONFIG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Null Sanitizing
app.add_middleware(SanitizeNullMiddleware)

# Routes
app.include_router(auth_router, prefix="/apistore/auth", tags=["Auth"])
app.include_router(product_router, prefix="/apistore/product", tags=["Product"])
# Root endpoint
@app.get("/root", tags=["Root"])
async def root():
    logger.debug("Root endpoint called")
    return { "message": "Thisai Courier API Store Running Successfully" }

# Global Exception Handlers
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
