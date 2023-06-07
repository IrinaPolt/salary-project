from datetime import datetime
from typing import Optional

from app.models.core import IDModelMixin, CoreModel


class PromotionBase(CoreModel):
    user_id: int
    position: str
    promotion_date: Optional[datetime]


class PromotionInDB(IDModelMixin, PromotionBase):
    user_id: int
    position: str
    promotion_date: Optional[datetime]


class PromotionPublic(IDModelMixin, PromotionBase):
    pass
