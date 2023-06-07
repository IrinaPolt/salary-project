from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED
from app.models.wages import WageBase, WagePublic
from app.db.repositories.wages import WagesRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.post("/", response_model=WagePublic, name="wages:create-wage", status_code=HTTP_201_CREATED)
async def create_new_wage(
    new_wage: WageBase = Body(..., embed=True),
    wages_repo: WagesRepository = Depends(get_repository(WagesRepository)),
) -> WagePublic:
    created_wage = await wages_repo.create_wage(new_wage=new_wage)
    return created_wage
