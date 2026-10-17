"""API REST avec FastAPI - SQUELETTE.
Lancer : uvicorn main:app --reload
Docs   : http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

import db

app = FastAPI(title="BiblioTech API", version="1.0.0")


@app.on_event("startup")
def startup():
    db.init_db()


# ---------- TODO : modeles Pydantic (validation) ----------
# BookIn     : id > 0, title et author non vides, available_copies >= 0, rental_price >= 0
# BookUpdate : comme BookIn, sans id
# BookOut    : comme BookIn


# ---------- TODO : endpoints ----------
# GET    /books          -> liste                (200)
# POST   /books          -> creation             (201, 409 si l'ID existe)
# PUT    /books/{id}     -> modification         (200, 404 si introuvable)
# DELETE /books/{id}     -> suppression          (204, 404 si introuvable)
# Utiliser db.py et HTTPException(status_code=..., detail=...)
