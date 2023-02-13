from db import db


class ContractModel(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    total_amount = db.Column(db.Float(precision=2),
                             unique=False,
                             nullable=False)
    duration = db.Column(db.String(40), unique=False, nullable=False)
    intrest = db.Column(db.Float(precision=2), unique=False, nullable=False)
    cash_kicks = db.relationship("CashKickModel",
                                 back_populates="contracts",
                                 secondary="cashkick_contracts")
