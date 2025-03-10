""" CLI Commands Factory """

from adm_server.ext.database import db
from adm_server.ext.database.models import *
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
    try:
        # Apagar todos os registros das tabelas
        db.session.query(EspTeste).delete()
        db.session.query(EspControle).delete()
        db.session.query(EspSala).delete()
        db.session.commit()  # Aplicar a mudança no banco de dados
        click.echo("Todas as linhas foram apagadas com sucesso.")
    except Exception as e:
        db.session.rollback()  # Reverter em caso de erro
        click.echo(f"Erro ao apagar as linhas: {e}")
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