from app.models.core import IDModelMixin, CoreModel


class UserBase(CoreModel):
    email: str
    first_name: str
    last_name: str

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {full_name!r}>".format(
            full_name=self.first_name + ' ' + self.last_name)


class UserCreate(UserBase):
    password: str


class UserInDb(IDModelMixin, UserBase):
    password_hash: bytes


class UserForSave(UserBase):
    password_hash: bytes
