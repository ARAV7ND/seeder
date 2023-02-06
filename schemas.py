from marshmallow import Schema, fields


class PlainContractSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    intrest = fields.Float(required=True)
    total_amount = fields.Float(required=True)
    duration = fields.Str(required=True)


class PlainUserDataSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone = fields.Int(required=True)
    address = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainCashKickSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    total_amount = fields.Float(required=True)
    status = fields.Str(required=True)


class CashKickSchema(PlainCashKickSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserDataSchema(), dump_only=True)


class UserDataSchema(PlainUserDataSchema):
    cash_kicks = fields.List(fields.Nested(PlainCashKickSchema()),
                             dump_only=True)


class ContractSchema(PlainContractSchema):
    cash_kicks = fields.List(fields.Nested(PlainContractSchema()),
                             dump_only=True)


class CashKikAndContractsSchema(Schema):
    message = fields.Str()
    cash_kick = fields.Nested(ContractSchema)
    contract = fields.Nested(ContractSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
