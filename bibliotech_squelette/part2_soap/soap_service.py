
"""Service SOAP avec Spyne - BiblioTech."""

from wsgiref.simple_server import make_server

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Fault
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import db

TNS = "http://bibliotech.example/soap"


class BookModel(ComplexModel):
    __namespace__ = TNS

    id = Integer
    title = Unicode
    author = Unicode
    available_copies = Integer
    rental_price = Float


def guard(func, *args):
    """Convertir les erreurs métier en erreurs SOAP."""
    try:
        return func(*args)
    except ValueError as exc:
        raise Fault(
            faultcode="Client.Validation",
            faultstring=str(exc),
        )
    except LookupError as exc:
        raise Fault(
            faultcode="Client.NotFound",
            faultstring=str(exc),
        )


def to_book_model(data):
    return BookModel(
        id=data["id"],
        title=data["title"],
        author=data["author"],
        available_copies=data["available_copies"],
        rental_price=data["rental_price"],
    )


class BookService(ServiceBase):

    @rpc(Integer, Unicode, Unicode, Integer, Float, _returns=BookModel)
    def CreateBook(ctx, id, title, author, available_copies, rental_price):
        result = guard(
            db.create_book,
            id, title, author, available_copies, rental_price,
        )
        return to_book_model(result)

    @rpc(Integer, _returns=BookModel)
    def GetBook(ctx, id):
        result = guard(db.get_book, id)
        return to_book_model(result)

    @rpc(Integer, Unicode, Unicode, Integer, Float, _returns=BookModel)
    def UpdateBook(ctx, id, title, author, available_copies, rental_price):
        result = guard(
            db.update_book,
            id, title, author, available_copies, rental_price,
        )
        return to_book_model(result)

    @rpc(Integer, _returns=Unicode)
    def DeleteBook(ctx, id):
        return guard(db.delete_book, id)


application = Application(
    [BookService],
    tns=TNS,
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_application = WsgiApplication(application)


if __name__ == "__main__":
    db.init_db()

    server = make_server("127.0.0.1", 8000, wsgi_application)

    print("Service SOAP démarré sur http://localhost:8000")
    print("WSDL disponible sur http://localhost:8000/?wsdl")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du service SOAP.")
        server.server_close()
