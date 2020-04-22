from marshmallow import Schema, fields


class PaymentSchema(Schema):
    payment_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    total_price = fields.Decimal(required=True)
    status = fields.Int(required=True)
