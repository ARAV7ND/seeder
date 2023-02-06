from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserDataSchema, UserSchema
from models.user_data import UserDataModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route("/user")
class User(MethodView):

    @blp.response(200, UserDataSchema(many=True))
    def get(self):
        users = UserDataModel.query.all()
        return users

    @blp.arguments(UserDataSchema)
    @blp.response(200, UserDataSchema)
    def post(self, user_data):
        user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
        user = UserDataModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        return user_data


@blp.route("/user/<string:user_id>")
class UserList(MethodView):

    @blp.response(200, UserDataSchema)
    def get(self, user_id):
        user = UserDataModel.query.get_or_404(user_id)
        return user

    @blp.arguments(UserDataSchema)
    @blp.response(200, UserDataSchema)
    def put(self, user_data, user_id):
        user = UserDataModel.query.get_or_404(user_id)
        if user:
            user.name = user_data["name"]
            user.address = user_data["address"]
            user.phone = user_data["phone"]
            user.username = user_data["username"]
            user.password = pbkdf2_sha256.hash(user_data["password"])
        else:
            user = UserDataModel(id=user_id, **user_data)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserDataModel.query.filter(
            UserDataModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["username"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid credentials")


@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
