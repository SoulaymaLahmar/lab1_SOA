
"""API REST BiblioTech.

Lancement : uvicorn main:app --reload
Documentation : http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

import db


class BookIn(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    available_copies: int = Field(ge=0)
    rental_price: float = Field(ge=0)

    model_config = ConfigDict(str_strip_whitespace=True)


class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    available_copies: int = Field(ge=0)
    rental_price: float = Field(ge=0)

    model_config = ConfigDict(str_strip_whitespace=True)


class BookOut(BookIn):
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="BiblioTech API",
    version="1.0.0",
    description="API REST de gestion des livres de la bibliotheque.",
    lifespan=lifespan,
)


def raise_not_found(exc):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


@app.get("/books", response_model=list[BookOut])
def get_books():
    return db.list_books()


@app.post(
    "/books",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookIn):
    try:
        return db.create_book(
            book.id,
            book.title,
            book.author,
            book.available_copies,
            book.rental_price,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@app.put("/books/{id}", response_model=BookOut)
def update_book(id: int, book: BookUpdate):
    if id <= 0:
        raise HTTPException(status_code=422, detail="ID invalide.")

    try:
        return db.update_book(
            id,
            book.title,
            book.author,
            book.available_copies,
            book.rental_price,
        )
    except LookupError as exc:
        raise_not_found(exc)


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    if id <= 0:
        raise HTTPException(status_code=422, detail="ID invalide.")

    try:
        db.delete_book(id)
    except LookupError as exc:
        raise_not_found(exc)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
