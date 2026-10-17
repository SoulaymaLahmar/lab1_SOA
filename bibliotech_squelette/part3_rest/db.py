
"""Couche de donnees SQLAlchemy pour BiblioTech."""

import os

from sqlalchemy import (
    create_engine, Column, Integer, String, Float
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://library:library@localhost:5432/library",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    available_copies = Column(Integer, nullable=False)
    rental_price = Column(Float, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def validate_book(book_id, title, author, copies, price):
    if isinstance(book_id, bool) or not isinstance(book_id, int) or book_id <= 0:
        raise ValueError("L'identifiant doit etre un entier positif.")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Le titre ne peut pas etre vide.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("L'auteur ne peut pas etre vide.")

    if isinstance(copies, bool) or not isinstance(copies, int) or copies < 0:
        raise ValueError("Le stock doit etre un entier positif ou nul.")

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Le prix doit etre positif ou nul.")


def book_to_dict(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "available_copies": book.available_copies,
        "rental_price": book.rental_price,
    }


def create_book(book_id, title, author, copies, price):
    validate_book(book_id, title, author, copies, price)

    with SessionLocal() as session:
        if session.get(Book, book_id) is not None:
            raise ValueError("Un livre avec cet identifiant existe deja.")

        book = Book(
            id=book_id,
            title=title.strip(),
            author=author.strip(),
            available_copies=copies,
            rental_price=price,
        )
        session.add(book)

        try:
            session.commit()
            session.refresh(book)
            return book_to_dict(book)
        except IntegrityError:
            session.rollback()
            raise ValueError("Un livre avec cet identifiant existe deja.")


def get_book(book_id):
    with SessionLocal() as session:
        book = session.get(Book, book_id)
        if book is None:
            raise LookupError("Livre introuvable.")
        return book_to_dict(book)


def list_books():
    with SessionLocal() as session:
        books = session.query(Book).order_by(Book.id).all()
        return [book_to_dict(book) for book in books]


def update_book(book_id, title, author, copies, price):
    validate_book(book_id, title, author, copies, price)

    with SessionLocal() as session:
        book = session.get(Book, book_id)
        if book is None:
            raise LookupError("Livre introuvable.")

        book.title = title.strip()
        book.author = author.strip()
        book.available_copies = copies
        book.rental_price = price

        session.commit()
        session.refresh(book)
        return book_to_dict(book)


def delete_book(book_id):
    with SessionLocal() as session:
        book = session.get(Book, book_id)
        if book is None:
            raise LookupError("Livre introuvable.")

        session.delete(book)
        session.commit()
