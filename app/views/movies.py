from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        request_movies = Movie.query
        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            request_movies = request_movies.filter(Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            request_movies = request_movies.filter(Movie.genre_id == genre_id)
        movies = request_movies.all()
        return movies_schema.dumps(movies, ensure_ascii=False), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid: int):
        try:
            movie_by_mid = Movie.query.get(mid)
            return movie_schema.dumps(movie_by_mid, ensure_ascii=False), 200
        except Exception as e:
            return "", 404

    def put(self, mid):
        movie = Movie.query.get(mid)
        req_json = request.json
        movie.name = req_json.get("name")
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


#movie_by_mid = Movie.query.get(2)
#print(movie_schema.dumps(movie_by_mid))