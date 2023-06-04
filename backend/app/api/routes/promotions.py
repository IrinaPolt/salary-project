from typing import List

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_all_promotions() -> List[dict]:
    promotions = [
        {"id": 1, "employee_name": "Adam Smith", "position": "chief executive officer", "promotion_date": "01.01.2025"},
        {"id": 2, "employee_name": "Marta Adams", "position": "head of department", "promotion_date": "31.12.2024"}
    ]

    return promotions

