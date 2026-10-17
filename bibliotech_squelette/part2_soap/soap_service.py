"""Service SOAP avec Spyne - SQUELETTE.
Lancer : python soap_service.py
WSDL   : http://localhost:8000/?wsdl
"""
from wsgiref.simple_server import make_server
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Fault
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import db

TNS = "http://bibliotech.example/soap"


# TODO : classe BookModel(ComplexModel) avec id, title, author, available_copies, rental_price
#        (n'oubliez pas __namespace__ = TNS)


def guard(func, *args):
    """TODO : appeler func(*args) ; transformer ValueError et LookupError en Fault SOAP."""
    raise NotImplementedError


class BookService(ServiceBase):
    # TODO : decorer chaque methode avec @rpc(types..., _returns=...)
    # Les noms des parametres doivent etre : id, title, author, available_copies, rental_price

    def CreateBook(ctx, id, title, author, available_copies, rental_price):
        pass

    def GetBook(ctx, id):
        pass

    def UpdateBook(ctx, id, title, author, available_copies, rental_price):
        pass

    def DeleteBook(ctx, id):
        pass


# TODO : application = Application([BookService], tns=TNS, in_protocol=..., out_protocol=...)

if __name__ == "__main__":
    # TODO : db.init_db(), creer le serveur WSGI sur le port 8000, serve_forever()
    pass
