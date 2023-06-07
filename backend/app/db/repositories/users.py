from app.db.repositories.base import BaseRepository
from app.models.users import UserForSave, UserInDb


CREATE_USER_QUERY = """
    INSERT INTO users (first_name, last_name, email, password_hash)
    VALUES (:first_name, :last_name, :email, :password_hash)
    RETURNING id, first_name, last_name, email, password_hash
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, first_name, last_name, email, password_hash
    FROM users
    WHERE email = :email
"""


class UsersRepository(BaseRepository):

    async def create_user(self, *, new_user: UserForSave) -> UserInDb:
        query_values = new_user.dict()
        user = await self.db.fetch_one(query=CREATE_USER_QUERY, values=query_values)

        return UserInDb(**user)

    async def get_user_by_email(self, email: str) -> UserInDb:
        user = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email": email})
        if user is None:
            return None

        return UserInDb(**user)
