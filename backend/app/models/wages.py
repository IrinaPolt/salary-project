from datetime import datetime
from typing import Optional

from app.models.core import IDModelMixin, CoreModel


class WageBase(CoreModel):
    user_id: int
    rate: float


class WageInDB(IDModelMixin, WageBase):
    user_id: int
    rate: float


class WagePublic(IDModelMixin, WageBase):
    pass
