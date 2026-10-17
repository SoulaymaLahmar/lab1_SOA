"""Couche donnees (SQLAlchemy) - SQUELETTE.
Reprenez la logique de la partie 1, mais SANS interface graphique.
Convention : ValueError = donnees invalides, LookupError = livre introuvable.
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://library:library@localhost:5432/library")
# TODO : engine, SessionLocal, Base


class Book:  # TODO : en faire un modele SQLAlchemy (herite de Base), table "books"
    pass


def init_db():
    # TODO : creer les tables
    raise NotImplementedError


def validate_book(book_id, title, author, copies, price):
    # TODO : ID invalide, stock negatif, prix negatif, titre/auteur vides -> ValueError
    raise NotImplementedError


def create_book(book_id, title, author, copies, price):
    raise NotImplementedError


def get_book(book_id):
    # LookupError si introuvable ; renvoie un dictionnaire
    raise NotImplementedError


def update_book(book_id, title, author, copies, price):
    raise NotImplementedError


def delete_book(book_id):
    raise NotImplementedError
