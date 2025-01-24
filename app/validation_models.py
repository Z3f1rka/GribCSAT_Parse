from pydantic import BaseModel


class Product(BaseModel):
    file: list
    link: str
    title: str
    type: str
    article: str
    shop: tuple[str, str]
    feedbacks: list[tuple[str, str, str, int]]


class FBLOUTPUT(Product):
    pass


class FBLINPUT(BaseModel):
    link: str
    count: int | None = None
