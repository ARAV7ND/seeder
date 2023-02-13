from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.cashkick_contracts import CashKickContractsModel
from schemas import CashKikAndContractsSchema

blp = Blueprint("cash_kick_contracts",
                __name__,
                description="Operation on cash_kick")


@blp.route("/cash_kick_contarcts")
class CashKickContracts(MethodView):

    @blp.response(200, CashKikAndContractsSchema(many=True))
    def get(self):
        return CashKickContractsModel.query.all()
