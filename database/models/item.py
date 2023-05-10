import decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import TimedBaseModel


class Item(TimedBaseModel):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(64))
    price: Mapped[decimal.Decimal | None] = mapped_column(Numeric(12, 2))
    tax: Mapped[decimal.Decimal | None] = mapped_column(Numeric(12, 2))
