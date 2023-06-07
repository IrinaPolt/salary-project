from app.db.repositories.base import BaseRepository
from app.models.promotions import PromotionBase, PromotionInDB


CREATE_PROMOTION_QUERY = """
    INSERT INTO promotions (employee_name, position, promotion_date)
    VALUES (:employee_name, :position, :promotion_date)
    RETURNING id, employee_name, position, promotion_date;
"""


class PromotionsRepository(BaseRepository):

    async def create_promotion(self, *, new_promotion: PromotionBase) -> PromotionInDB:
        query_values = new_promotion.dict()
        promotion = await self.db.fetch_one(query=CREATE_PROMOTION_QUERY, values=query_values)

        return PromotionInDB(**promotion)
