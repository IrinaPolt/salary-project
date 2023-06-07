from fastapi import APIRouter

from app.api.routes.promotions import router as promotions_router
from app.api.routes.wages import router as wages_router
from app.api.routes.users import router as users_router

router = APIRouter()


router.include_router(promotions_router, prefix="/promotions", tags=["promotions"])
router.include_router(wages_router, prefix="/wages", tags=["wages"])
router.include_router(users_router, prefix="/users", tags=["users"])
