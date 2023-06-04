from fastapi import APIRouter

from app.api.routes.promotions import router as promotions_router


router = APIRouter()


router.include_router(promotions_router, prefix="/promotions", tags=["promotions"])

