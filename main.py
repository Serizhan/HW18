# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример
from flask_restx import Api

from app.config import Config
from flask import Flask
from app.database import db

# from config import Config
# from models import Review, Book
# from setup_db import db

#
# функция создания основного объекта app
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns


def create_app(config_object: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()
    return application


#
# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    create_data(application, db)


#
#
# функция
def create_data(app, db):
    with app.app_context():
        db.create_all()

        #         создать несколько сущностей чтобы добавить их в БД
        #
        with db.session.begin():
            db.session.add_all()


#


if __name__ == '__main__':
    app = create_app(Config())
    register_extensions(app)
    app.run()
