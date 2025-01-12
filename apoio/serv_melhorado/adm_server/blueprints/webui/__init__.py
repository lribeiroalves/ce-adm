""" WebUI Blueprint Factory """

from flask import Blueprint

from .views import *

bp = Blueprint('webui', __name__)

# URLs para visualização do usuário
bp.add_url_rule('/', methods = ['GET'], view_func = index)


def init_app(app):
    app.register_blueprint(bp)