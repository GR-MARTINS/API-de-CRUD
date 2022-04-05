from itertools import count
from typing import Optional
from pydantic import BaseModel, Field

c = count()


class Book(BaseModel):
    #id: Optional[int] = Field(defaul_factory=lambda: next(c))
    livro: str
    escritor: str


class ListBooks(BaseModel):
    count: int
    books: list[Book]


class ListIdBooks(BaseModel):
    """
    Lista de id's a serem excluídos
    """
    list: list[int]

class User(BaseModel):
    #id: Optional[int] = Field(defaul_factory=lambda: next(c))
    username: str
    password: str


class Login(BaseModel):
    #id: Optional[int] = Field(defaul_factory=lambda: next(c))
    username: str
    password: str