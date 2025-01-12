""" App Factory da Base de Dados"""
""" Flask SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)
    app.teardown_appcontext(lambda exc: db.session.close()) # Encerra a session da base de dados sempre que um contexto da aplicação Flask é encerrado