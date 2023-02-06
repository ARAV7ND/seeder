from db import db


class CashKickContractsModel(db.Model):
    __tablename__ = "cashkick_contracts"

    id = db.Column(db.Integer, primary_key=True)
    cash_kick_id = db.Column(db.Integer, db.ForeignKey("cash_kicks.id"))
    contracts_id = db.Column(db.Integer, db.ForeignKey("contracts.id"))
