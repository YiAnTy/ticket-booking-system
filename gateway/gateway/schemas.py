from marshmallow import Schema, fields


class CreateAccountSchema(Schema):
    user_name = fields.Str(required=True)


class GetAccountSchema(Schema):
    account_id = fields.Int(required=True)
    user_name = fields.Str(required=True)


class CreateOrderDetailSchema(Schema):
    ticket_id = fields.Str(required=True)
    price = fields.Decimal(as_string=True, required=True)


class CreateOrderSchema(Schema):
    order_details = fields.Nested(
        CreateOrderDetailSchema, many=True, required=True
    )
    account_id = fields.Int(required=True)
    status = fields.Int(required=True)


class TicketSchema(Schema):
    ticket_id = fields.Str(required=True)
    title = fields.Str(required=True)
    status = fields.Str(required=True)


class GetOrderSchema(Schema):

    class OrderDetail(Schema):
        id = fields.Int()
        ticket_id = fields.Str()
        price = fields.Decimal(as_string=True)
        ticket = fields.Nested(TicketSchema, many=False)

    id = fields.Int()
    account_id = fields.Int()
    status = fields.Int()
    order_details = fields.Nested(OrderDetail, many=True)


class GetPaymentSchema(Schema):
    payment_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    total_price = fields.Decimal(as_string=True)
    status = fields.Int(required=True)
