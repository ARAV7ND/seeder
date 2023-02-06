from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ContractSchema
from models.contract import ContractModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import get_jwt, jwt_required

blp = Blueprint("contracts", __name__, description="Operation on contracts")


@blp.route("/contracts")
class ContractList(MethodView):

    @blp.response(200, ContractSchema(many=True))
    def get(self):
        return ContractModel.query.all()

    @jwt_required()
    @blp.arguments(ContractSchema)
    @blp.response(200, ContractSchema)
    def post(self, contract_data):
        contract = ContractModel(**contract_data)
        try:
            db.session.add(contract)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="A contract with that name already exists")
        except SQLAlchemyError as e:
            abort(500,
                  message=f"An Error occured while inserting the Contract {e}")
        return contract


@blp.route("/contracts/<string:contract_id>")
class Contract(MethodView):

    @blp.response(200, ContractSchema)
    def get(self, contract_id):
        contract = ContractModel.query.get_or_404(contract_id)
        return contract

    @jwt_required()
    @blp.arguments(ContractSchema)
    @blp.response(201, ContractSchema)
    def put(self, contract_data, contract_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required")
        contract = ContractModel.query.get_or_404(contract_id)
        if contract:
            contract.name = contract_data["name"]
            contract.intrest = contract_data["intrest"]
            contract.total_amount = contract_data["total_amount"]
            contract.duration = contract_data["duration"]
        else:
            contract = ContractModel(id=contract_id, **contract_data)
        db.session.add(contract)
        db.session.commit()
        return contract

    @jwt_required()
    @blp.response(
        202,
        description=
        "Deletes a contract if cash kicks is not associated with it.",
        example={"message": "cash kick deleted"})
    @blp.alt_response(
        400,
        description=
        "Returned if the contract is assigned to one or more cash kicks. In this case, contract is not deleted"
    )
    def delete(self, contract_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required")
        contract = ContractModel.query.get_or_404(contract_id)
        if not contract.cash_kicks:
            db.session.delete(contract)
            db.session.commit()
            return {"message": "Contarct deleted"}
        abort(
            400,
            message=
            "could not delete contarct. Make sure contracts is not associated with any cash kick, then try again"
        )