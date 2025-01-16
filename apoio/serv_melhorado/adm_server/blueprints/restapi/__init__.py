from flask import Blueprint
from flask_restful import Api
from .resources import *

bp = Blueprint('restapi', __name__, url_prefix='/api/v1')
api = Api(bp)

api.add_resource(FullDatabaseResource, '/packets')
api.add_resource(LastRegister, '/last-packet')

def init_app(app):
    app.register_blueprint(bp)
