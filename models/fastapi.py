from pydantic import BaseModel


class MyItem(BaseModel):
    id: int | None = None
    name: str | None
    description: str | None
    price: float | None
    tax: float | None
