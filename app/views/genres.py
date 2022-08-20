from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dumps(all_genres, ensure_ascii=False), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre_by_did = Genre.query.get(gid)
            return genre_schema.dumps(genre_by_did, ensure_ascii=False), 200
        except Exception as e:
            return "", 404

    def put(self, gid):
        genre = Genre.query.get(gid)
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204