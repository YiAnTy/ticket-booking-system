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


class TicketSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)


class GetOrderSchema(Schema):

    class OrderDetail(Schema):
        id = fields.Int()
        ticket_id = fields.Str()
        price = fields.Decimal(as_string=True)
        ticket = fields.Nested(TicketSchema, many=False)

    id = fields.Int()
    order_details = fields.Nested(OrderDetail, many=True)
