""" Configurar o App Factory """

from flask import Flask
import os
from .ext import configuration


def create_app():
    template_dir = os.path.abspath('adm_server/blueprints/webui/templates')
    static_dir = os.path.abspath('adm_server/blueprints/webui/static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    configuration.init_app(app)

    return app

