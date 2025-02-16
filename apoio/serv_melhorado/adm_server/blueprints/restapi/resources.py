from flask import jsonify, abort
from flask_restful import Resource
from adm_server.ext.database import db
from adm_server.ext.database.models import *


class FullDatabaseResource(Resource):
    def get(self):
        packets_received = db.session.execute(
            db.select(EspTeste)
        ).scalars().all() or abort(204)

        return jsonify(
            {'pacotes_recebidos': [packet.to_dict() for packet in packets_received]}
        )


class LastRegister(Resource):
    def get(self):
        last_register = db.session.execute(
            db.select(EspTeste).order_by(EspTeste.id.desc())
        ).scalars().first() or abort(204)

        return jsonify(
            last_register.to_dict()
        )