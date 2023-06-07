from fastapi import APIRouter, Body, Depends
from passlib.context import CryptContext
from starlette.status import HTTP_201_CREATED

from app.models.users import UserBase, UserForSave, UserCreate, UserInDb
from app.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository


router = APIRouter()
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=UserInDb, name="users:create-user", status_code=HTTP_201_CREATED)
async def create_new_user(
    new_user: UserCreate = Body(..., embed=True),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInDb:
    hashed_password = password_hasher.hash(new_user.password)
    user_for_save = UserForSave(
        email=new_user.email,
        password_hash=hashed_password,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
    )
    created_user = await users_repo.create_user(new_user=user_for_save)
    return created_user
