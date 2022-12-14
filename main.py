# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

from flask_restx import Api

from app.config import Config
from flask import Flask
from app.database import db

# функция создания основного объекта app
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from create_data import create_base


def create_app(config_object: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app: Flask):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    create_base()


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    app.run()
