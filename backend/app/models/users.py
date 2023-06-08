from datetime import datetime

from app.models.core import IDModelMixin, CoreModel


class UserBase(CoreModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserInDb(IDModelMixin, UserBase):
    password_hash: bytes


class UserForSave(UserBase):
    password_hash: bytes


class UserInfo(CoreModel):
    first_name: str
    last_name: str
    rate: float
    position: str
    promotion_date: datetime
