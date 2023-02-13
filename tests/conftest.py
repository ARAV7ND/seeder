from pytest import fixture

from app import create_app
from db import db


@fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()

    yield app


@fixture()
def client(app):
    return app.test_client()
