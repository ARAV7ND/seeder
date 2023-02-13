from db import db


class UserDataModel(db.Model):
    __tablename__ = "users_data"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cash_kicks = db.relationship("CashKickModel",
                                 back_populates="users",
                                 lazy="dynamic")
