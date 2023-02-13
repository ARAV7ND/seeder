from db import db


class CashKickModel(db.Model):
    __tablename__ = "cash_kicks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False)
    total_amount = db.Column(db.Float(precision=2),
                             unique=False,
                             nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users_data.id"),
                        unique=False,
                        nullable=False)
    users = db.relationship("UserDataModel", back_populates="cash_kicks")

    contracts = db.relationship(
        "ContractModel",
        back_populates="cash_kicks",
        secondary="cashkick_contracts",
    )
