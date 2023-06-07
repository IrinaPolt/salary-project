from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED
from app.models.promotions import PromotionBase, PromotionPublic
from app.db.repositories.promotions import PromotionsRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.post("/", response_model=PromotionPublic, name="promotions:create-promotion", status_code=HTTP_201_CREATED)
async def create_new_promotion(
    new_promotion: PromotionBase = Body(..., embed=True),
    promotions_repo: PromotionsRepository = Depends(get_repository(PromotionsRepository)),
) -> PromotionPublic:
    created_promotion = await promotions_repo.create_promotion(new_promotion=new_promotion)
    return created_promotion
