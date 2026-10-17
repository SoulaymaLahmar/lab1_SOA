
"""Couche donnees (SQLAlchemy) - BiblioTech."""

import os

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://library:library@localhost:5432/library"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    available_copies = Column(Integer, nullable=False)
    rental_price = Column(Float, nullable=False)


def init_db():
    """Creer les tables necessaires."""
    Base.metadata.create_all(bind=engine)


def validate_book(book_id, title, author, copies, price):
    """Lever ValueError si les donnees sont invalides."""
    if not isinstance(book_id, int) or isinstance(book_id, bool) or book_id <= 0:
        raise ValueError("L'identifiant doit etre un entier positif.")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Le titre est obligatoire.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("L'auteur est obligatoire.")

    if not isinstance(copies, int) or isinstance(copies, bool) or copies < 0:
        raise ValueError("Le stock doit etre un entier positif ou nul.")

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Le prix doit etre numerique.")

    if price < 0:
        raise ValueError("Le prix ne peut pas etre negatif.")


def create_book(book_id, title, author, copies, price):
    validate_book(book_id, title, author, copies, price)

    with SessionLocal() as session:
        if session.get(Book, book_id) is not None:
            raise ValueError("Un livre avec cet ID existe deja.")

        book = Book(
            id=book_id,
            title=title.strip(),
            author=author.strip(),
            available_copies=copies,
            rental_price=price
        )

        session.add(book)
        session.commit()
        session.refresh(book)

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "available_copies": book.available_copies,
            "rental_price": book.rental_price
        }


def get_book(book_id):
    if not isinstance(book_id, int) or isinstance(book_id, bool) or book_id <= 0:
        raise ValueError("L'identifiant doit etre un entier positif.")

    with SessionLocal() as session:
        book = session.get(Book, book_id)

        if book is None:
            raise LookupError("Livre introuvable.")

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "available_copies": book.available_copies,
            "rental_price": book.rental_price
        }


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

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "available_copies": book.available_copies,
            "rental_price": book.rental_price
        }


def delete_book(book_id):
    if not isinstance(book_id, int) or isinstance(book_id, bool) or book_id <= 0:
        raise ValueError("L'identifiant doit etre un entier positif.")

    with SessionLocal() as session:
        book = session.get(Book, book_id)

        if book is None:
            raise LookupError("Livre introuvable.")

        session.delete(book)
        session.commit()

        return "Livre supprime avec succes."
