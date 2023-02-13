from flask import Flask, jsonify
from flask_smorest import Api
from resources.user import blp as UserDataBlueprint
from resources.contract import blp as ContractBlueprint
from resources.cash_kick import blp as CashKickBlueprint
from resources.cash_kick_contracts import blp as CashKickContarctsBlueprint
from blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager
from db import db
import os
from dotenv import load_dotenv
import models

load_dotenv()

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "seeder"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "description": "The token has been revoked.",
                "error": "token_revoked"
            }),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has expired.",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed.",
                "error": "invalid_token"
            }),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }),
            401,
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(UserDataBlueprint)
    api.register_blueprint(ContractBlueprint)
    api.register_blueprint(CashKickBlueprint)
    api.register_blueprint(CashKickContarctsBlueprint)
    return app