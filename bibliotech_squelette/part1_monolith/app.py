
"""
Partie 1 - Version monolithique
BiblioTech : SQLAlchemy + PostgreSQL + PyQt5

Lancer :
    docker compose up -d
    python app.py
"""

import sys

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)


# ---------- TODO 1 : connexion à PostgreSQL ----------

DATABASE_URL = "postgresql+psycopg2://library:library@localhost:5432/library"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ---------- TODO 2 : table Book ----------

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    available_copies = Column(Integer, nullable=False)
    rental_price = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "available_copies": self.available_copies,
            "rental_price": self.rental_price,
        }


# Création de la table si elle n'existe pas
Base.metadata.create_all(bind=engine)


# ---------- TODO 4 : validation ----------

def validate(book_id, title, author, copies, price):
    """Vérifie les données du livre."""

    if book_id <= 0:
        raise ValueError("L'ID doit être strictement positif.")

    if not title.strip():
        raise ValueError("Le titre ne peut pas être vide.")

    if not author.strip():
        raise ValueError("L'auteur ne peut pas être vide.")

    if copies < 0:
        raise ValueError("Le nombre d'exemplaires ne peut pas être négatif.")

    if price < 0:
        raise ValueError("Le tarif ne peut pas être négatif.")


# ---------- TODO 3 : CRUD ----------

def create_book(book_id, title, author, copies, price):
    """Ajoute un livre dans la base de données."""

    validate(book_id, title, author, copies, price)

    with SessionLocal() as session:
        try:
            # Vérifier si l'ID existe déjà
            existing = session.get(Book, book_id)

            if existing is not None:
                raise ValueError(
                    f"Un livre avec l'ID {book_id} existe déjà."
                )

            book = Book(
                id=book_id,
                title=title.strip(),
                author=author.strip(),
                available_copies=copies,
                rental_price=price,
            )

            session.add(book)
            session.commit()

        except Exception:
            session.rollback()
            raise


def get_all_books():
    """Retourne tous les livres triés par ID."""

    with SessionLocal() as session:
        books = (
            session.query(Book)
            .order_by(Book.id)
            .all()
        )

        return [book.to_dict() for book in books]


def update_book(book_id, title, author, copies, price):
    """Modifie un livre existant."""

    validate(book_id, title, author, copies, price)

    with SessionLocal() as session:
        try:
            book = session.get(Book, book_id)

            if book is None:
                raise ValueError(
                    f"Aucun livre trouvé avec l'ID {book_id}."
                )

            book.title = title.strip()
            book.author = author.strip()
            book.available_copies = copies
            book.rental_price = price

            session.commit()

        except Exception:
            session.rollback()
            raise


def delete_book(book_id):
    """Supprime un livre existant."""

    with SessionLocal() as session:
        try:
            book = session.get(Book, book_id)

            if book is None:
                raise ValueError(
                    f"Aucun livre trouvé avec l'ID {book_id}."
                )

            session.delete(book)
            session.commit()

        except Exception:
            session.rollback()
            raise


# ---------- TODO 5 : interface PyQt5 ----------

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiblioTech - Monolithe")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        # Tableau des livres
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Titre",
            "Auteur",
            "Exemplaires",
            "Tarif",
        ])

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.table.cellClicked.connect(
            self.select_row
        )

        layout.addWidget(self.table)

        # Champs de saisie
        self.id_in = QLineEdit()
        self.title_in = QLineEdit()
        self.author_in = QLineEdit()
        self.copies_in = QLineEdit()
        self.price_in = QLineEdit()

        self.fields = [
            self.id_in,
            self.title_in,
            self.author_in,
            self.copies_in,
            self.price_in,
        ]

        form = QFormLayout()

        labels = [
            "ID",
            "Titre",
            "Auteur",
            "Exemplaires",
            "Tarif",
        ]

        for label, widget in zip(labels, self.fields):
            form.addRow(label, widget)

        layout.addLayout(form)

        # Boutons CRUD
        buttons = QHBoxLayout()

        actions = [
            ("Ajouter", self.add),
            ("Modifier", self.edit),
            ("Supprimer", self.remove),
            ("Rafraîchir", self.refresh),
        ]

        for text, action in actions:
            btn = QPushButton(text)
            btn.clicked.connect(action)
            buttons.addWidget(btn)

        layout.addLayout(buttons)

        # Chargement initial
        self.refresh()

    def read_form(self):
        """Lit les champs et convertit les types."""

        try:
            book_id = int(self.id_in.text())
            title = self.title_in.text()
            author = self.author_in.text()
            copies = int(self.copies_in.text())
            price = float(self.price_in.text())

        except ValueError:
            raise ValueError(
                "Vérifiez les champs numériques : "
                "ID, exemplaires et tarif."
            )

        validate(book_id, title, author, copies, price)

        return book_id, title, author, copies, price

    def add(self):
        """Ajoute un livre."""

        try:
            values = self.read_form()
            create_book(*values)

            self.refresh()
            self.clear_form()

            QMessageBox.information(
                self,
                "Succès",
                "Livre ajouté avec succès.",
            )

        except ValueError as error:
            QMessageBox.warning(
                self, "Erreur de saisie", str(error)
            )

        except SQLAlchemyError as error:
            QMessageBox.warning(
                self,
                "Erreur de base de données",
                str(error),
            )

    def edit(self):
        """Modifie le livre correspondant à l'ID saisi."""

        try:
            values = self.read_form()
            update_book(*values)

            self.refresh()
            self.clear_form()

            QMessageBox.information(
                self,
                "Succès",
                "Livre modifié avec succès.",
            )

        except ValueError as error:
            QMessageBox.warning(
                self, "Erreur de saisie", str(error)
            )

        except SQLAlchemyError as error:
            QMessageBox.warning(
                self,
                "Erreur de base de données",
                str(error),
            )

    def remove(self):
        """Supprime le livre correspondant à l'ID saisi."""

        try:
            book_id = int(self.id_in.text())

            answer = QMessageBox.question(
                self,
                "Confirmation",
                f"Supprimer le livre ID {book_id} ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if answer != QMessageBox.Yes:
                return

            delete_book(book_id)

            self.refresh()
            self.clear_form()

            QMessageBox.information(
                self,
                "Succès",
                "Livre supprimé avec succès.",
            )

        except ValueError as error:
            QMessageBox.warning(
                self, "Erreur", str(error)
            )

        except SQLAlchemyError as error:
            QMessageBox.warning(
                self,
                "Erreur de base de données",
                str(error),
            )

    def refresh(self):
        """Recharge les livres dans le tableau."""

        try:
            books = get_all_books()

            self.table.setRowCount(0)

            for book in books:
                row = self.table.rowCount()
                self.table.insertRow(row)

                values = [
                    book["id"],
                    book["title"],
                    book["author"],
                    book["available_copies"],
                    f'{book["rental_price"]:.2f}',
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, column, item)

            self.table.resizeColumnsToContents()

        except SQLAlchemyError as error:
            QMessageBox.warning(
                self,
                "Erreur de base de données",
                str(error),
            )

    def select_row(self, row, column):
        """Remplit le formulaire au clic sur une ligne."""

        values = []

        for col in range(5):
            item = self.table.item(row, col)
            values.append(item.text() if item else "")

        for field, value in zip(self.fields, values):
            field.setText(value)

    def clear_form(self):
        """Vide les champs du formulaire."""

        for field in self.fields:
            field.clear()


# ---------- Lancement de l'application ----------

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
