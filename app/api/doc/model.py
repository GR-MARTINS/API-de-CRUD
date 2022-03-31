from itertools import count
from typing import Optional
from pydantic import BaseModel, Field

c = count()


class BookPydantic(BaseModel):
    #id: Optional[int] = Field(defaul_factory=lambda: next(c))
    livro: str
    escritor: str


class ListBooksPydantic(BaseModel):
    count: int
    books: list[BookPydantic]


class ListIdBooksPydantic(BaseModel):
    """
    Lista de id's a serem excluídos
    """
    list: list[int]
