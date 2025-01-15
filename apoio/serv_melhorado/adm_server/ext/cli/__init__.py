""" CLI Commands Factory """

from adm_server.ext.database import db
from adm_server.ext.database.models import Readings, EspSensor
from adm_server.ext.mqtt import client_mqtt

from flask.cli import with_appcontext
import click
import datetime
import sys


def end_app():
    client_mqtt.disconnect() # Ao disconectar do broker o método loop forever retorna
    sys.exit(0) # Encerra a aplicação


def create_db():
    """ Criar a base de dados vazia """
    db.create_all()
    click.echo('Database criada.')
    end_app()


def drop_db():
    """ Destroi a base de dados """
    db.drop_all()
    click.echo('Database destruida.')
    end_app()


def clear_db():
    """ Limpa os dados mas mantém a tabela """
    db.drop_all()
    db.create_all()
    click.echo('Database restaurada.')
    end_app()


def populate_db():
    """ Cria uma população de teste para testar a base de dados """
    data = Readings(pacote = 1, name = 'esp32', led = True, adc = 4095, date = datetime.datetime.now())
    db.session.add(data)
    db.session.commit()
    click.echo('Database populada para testes')
    end_app()


def init_app(app):
    for com in [create_db, drop_db, populate_db, clear_db]:
        app.cli.add_command(app.cli.command()(com))