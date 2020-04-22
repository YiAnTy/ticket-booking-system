from marshmallow import Schema, fields


class OrderDetailSchema(Schema):
    id = fields.Int(required=True)
    ticket_id = fields.Str(required=True)
    price = fields.Decimal(as_string=True)


class OrderSchema(Schema):
    id = fields.Int(required=True)
    account_id = fields.Int(required=True)
    status = fields.Int(required=True)
    order_details = fields.Nested(OrderDetailSchema, many=True)
