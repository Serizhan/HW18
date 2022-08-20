from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        all_director = Director.query.all()
        return directors_schema.dumps(all_director, ensure_ascii=False), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director_by_did = Director.query.get(did)
            return director_schema.dumps(director_by_did, ensure_ascii=False), 200
        except Exception as e:
            return "", 404

    def put(self, did):
        director = Director.query.get(did)
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, did: int):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        return "", 204
