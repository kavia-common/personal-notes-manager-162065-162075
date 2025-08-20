from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.db.session import init_db
from src.routers import auth as auth_router
from src.routers import notes as notes_router
from src.routers import system as system_router


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function constructs the FastAPI app instance, loads configuration from
    environment variables, configures CORS, includes all API routers, and initializes
    the database connection.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title="Notes Backend API",
        description=(
            "Backend for a personal notes application. Provides user authentication "
            "and CRUD operations for notes with search functionality."
        ),
        version="1.0.0",
        openapi_tags=[
            {"name": "system", "description": "System/health endpoints"},
            {"name": "auth", "description": "User authentication endpoints"},
            {"name": "notes", "description": "Notes CRUD and search endpoints"},
        ],
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(system_router.router, prefix="", tags=["system"])
    app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
    app.include_router(notes_router.router, prefix="/notes", tags=["notes"])

    # Initialize database
    init_db()

    return app
