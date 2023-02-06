from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import CashKickSchema
from models.cash_kick import CashKickModel
from models.user_data import UserDataModel
from models.contract import ContractModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import get_jwt, jwt_required

blp = Blueprint("cash_kick", __name__, description="Operation on cash_kick")


@blp.route("/cash_kick")
class CashKickList(MethodView):

    @blp.response(200, CashKickSchema(many=True))
    def get(self):
        return CashKickModel.query.all()

    @blp.arguments(CashKickSchema)
    @blp.response(201, CashKickSchema)
    def post(self, cash_kick_data):
        print("user::", cash_kick_data)
        user_data = UserDataModel.query.get_or_404(cash_kick_data["user_id"])
        if user_data:
            cash_kick = CashKickModel(**cash_kick_data)
            try:
                db.session.add(cash_kick)
                db.session.commit()
            except IntegrityError as e:
                abort(400, message=str(e))
            except SQLAlchemyError as e:
                abort(400, message=str(e))
            return cash_kick
        else:
            abort(404, message="invalid userid")


@blp.route("/cash_kicks/<string:cash_kick_id>/contracts/<string:contract_id>")
class LinkCashKickAndContracts(MethodView):

    @blp.response(201, CashKickSchema)
    def post(self, contract_id, cash_kick_id):
        cash_kick = CashKickModel.query.get_or_404(cash_kick_id)
        contract = ContractModel.query.get_or_404(contract_id)

        cash_kick.contracts.append(contract)

        try:
            db.session.add(cash_kick)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return cash_kick

    @jwt_required()
    @blp.response(201, CashKickSchema)
    def delete(self, contract_id, cash_kick_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required")
        cash_kick = CashKickModel.query.get_or_404(cash_kick_id)
        contract = ContractModel.query.get_or_404(contract_id)
        cash_kick.contracts.append(contract)
        try:
            db.session.add(cash_kick)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {
            "message": "contract removed from cash_kick",
            "contract": contract,
            "cash_kick": cash_kick
        }


@blp.route("/cash_kick/<string:cash_kick_id>")
class CashKick(MethodView):

    @jwt_required()
    @blp.response(200, CashKickSchema)
    def get(self, cash_kick_id):
        cash_kick = CashKickModel.query.get_or_404(cash_kick_id)
        return cash_kick

    @jwt_required()
    @blp.response(
        202,
        description="Deletes a cash kick if contract is associated with it.",
        example={"message": "cash kick deleted"})
    @blp.alt_response(
        400,
        description=
        "Returned if the cash kick is assigned to one or more. In this case, cash kick is not deleted"
    )
    def delete(self, cash_kick_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required")
        cash_kick = CashKickModel.query.get_or_404(cash_kick_id)

        if not cash_kick.contracts:
            db.session.delete(cash_kick)
            db.session.commit()
            return {"message": "cash_kick deleted"}
        abort(
            400,
            message=
            "could not delete cash_kick. Make sure cash kick is not associated with any contracts, then try again"
        )

    @blp.arguments(CashKickSchema)
    @blp.response(200, CashKickSchema)
    def put(self, cash_kick_data, cash_kick_id):
        cash_kick = CashKickModel.query.get_or_404(cash_kick_id)
        if cash_kick:
            cash_kick.user_id = cash_kick_data["user_id"]
            cash_kick.name = cash_kick_data["name"]
            cash_kick.total_amount = cash_kick_data["total_amount"]
            cash_kick.status = cash_kick_data["status"]
        else:
            cash_kick = CashKickModel(id=cash_kick_id, **cash_kick_data)
        db.session.add(cash_kick)
        db.session.commit()
        return cash_kick