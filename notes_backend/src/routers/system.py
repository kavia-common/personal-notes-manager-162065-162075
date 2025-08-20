from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Health Check",
    description="Simple health check endpoint.",
)
# PUBLIC_INTERFACE
def health_check():
    """Return a basic health status."""
    return {"message": "Healthy"}
