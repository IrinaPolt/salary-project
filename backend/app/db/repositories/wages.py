from app.db.repositories.base import BaseRepository
from app.models.wages import WageBase, WageInDB


CREATE_WAGE_QUERY = """
    INSERT INTO wages (user_id, rate)
    VALUES (:user_id, :rate)
    RETURNING id, user_id, rate;
"""


class WagesRepository(BaseRepository):

    async def create_wage(self, *, new_wage: WageBase) -> WageInDB:
        query_values = new_wage.dict()
        wage = await self.db.fetch_one(query=CREATE_WAGE_QUERY, values=query_values)

        return WageInDB(**wage)
