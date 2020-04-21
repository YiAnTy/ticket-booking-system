import json
from nameko.exceptions import BadRequest
from werkzeug import Response
from flask import Flask, request, jsonify
from nameko.standalone.rpc import ClusterRpcProxy
import argparse

from gateway.gateway.exceptions import TicketNotFound
from gateway.gateway.schemas import CreateAccountSchema, GetAccountSchema, CreateOrderSchema, GetOrderSchema, TicketSchema


parser = argparse.ArgumentParser()
parser.add_argument("--port", help="app running port", type=int, default=5000)
parse_args = parser.parse_args()

app = Flask(__name__)

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


"""
Service acts as a gateway to other services over http.
"""

name = 'gateway'


ClusterRpcProxy(CONFIG)


@app.route('/tickets', methods=["GET"])
def get_product():
    """Gets ticket by `ticket_id`
    """
    ticket_id = request.args.get("ticket_id")
    with ClusterRpcProxy(CONFIG) as rpc:
        product = rpc.ticketService.get(ticket_id)
    return Response(
        TicketSchema().dumps(product),
        mimetype='application/json'
    )


@app.route('/tickets', methods=["POST"])
def create_product():
    """Create a new product - product data is posted as json

    Example request ::

        {
            "id": "the_odyssey",
            "title": "The Odyssey",
            "passenger_capacity": 101,
            "maximum_speed": 5,
            "in_stock": 10
        }


    The response contains the new product ID in a json document ::

        {"id": "the_odyssey"}

    """

    schema = TicketSchema()

    try:
        # load input data through a schema (for validation)
        # Note - this may raise `ValueError` for invalid json,
        # or `ValidationError` if data is invalid.
        ticket_data = schema.loads(request.get_data(as_text=True))
    except ValueError as exc:
        raise BadRequest("Invalid json: {}".format(exc))

    # Create the product
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.ticketService.create(ticket_data)
    return Response(
        json.dumps({'id': ticket_data['id']}), mimetype='application/json'
    )


@app.route('/orders', methods=["GET"])
def get_order():
    """Gets the order details for the order given by `order_id`.

    Enhances the order details with full product details from the
    products-service.
    """
    order = _get_order(request.args.get("order_id"))
    return Response(
        GetOrderSchema().dumps(order),
        mimetype='application/json'
    )


def _get_order(order_id):
    # Retrieve order data from the orders service.
    # Note - this may raise a remote exception that has been mapped to
    # raise``OrderNotFound``
    with ClusterRpcProxy(CONFIG) as rpc:
        order = rpc.orderService.get_order(order_id)

        # Retrieve all products from the products service
        ticket_map = {prod['id']: prod for prod in rpc.ticketService.list()}


    # Enhance order details with product and image details.
    for item in order['order_details']:
        ticket_id = item['ticket_id']

        item['ticket'] = ticket_map[ticket_id]

    return order


@app.route('/orders', methods=["POST"])
def create_order():
    """Create a new order - order data is posted as json

    Example request ::

        {
            "order_details": [
                {
                    "product_id": "the_odyssey",
                    "price": "99.99",
                    "quantity": 1
                },
                {
                    "price": "5.99",
                    "product_id": "the_enigma",
                    "quantity": 2
                },
            ]
        }


    The response contains the new order ID in a json document ::

        {"id": 1234}

    """

    schema = CreateOrderSchema()

    try:
        # load input data through a schema (for validation)
        # Note - this may raise `ValueError` for invalid json,
        # or `ValidationError` if data is invalid.
        order_data = schema.loads(request.get_data(as_text=True))
    except ValueError as exc:
        raise BadRequest("Invalid json: {}".format(exc))

    # Create the order
    # Note - this may raise `ProductNotFound`
    id_ = _create_order(order_data)
    return Response(json.dumps({'id': id_}), mimetype='application/json')


def _create_order(order_data):
    # check order product ids are valid
    with ClusterRpcProxy(CONFIG) as rpc:
        valid_ticket_ids = {prod['id'] for prod in rpc.ticketService.list()}
        for item in order_data['order_details']:
            if item['ticket_id'] not in valid_ticket_ids:
                raise TicketNotFound(
                    "ticket Id {}".format(item['ticket_id'])
                )

        # Call orders-service to create the order.
        # Dump the data through the schema to ensure the values are serialized
        # correctly.
        serialized_data = CreateOrderSchema().dump(order_data)
        result = rpc.orderService.create_order(
            serialized_data['order_details']
        )
        return result['id']


@app.route('/accounts', methods=['POST'])
def add_account():
    schema = CreateAccountSchema()
    try:
        # load input data through a schema (for validation)
        # Note - this may raise `ValueError` for invalid json,
        # or `ValidationError` if data is invalid.
        account_data = schema.loads(request.get_data(as_text=True))
    except ValueError as exc:
        raise BadRequest("Invalid json: {}".format(exc))

    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.userService.add_account(account_data)
    return Response(json.dumps({'id': result['account_id']}), mimetype='application/json')


@app.route('/accounts', methods=['GET'])
def get_account():
    with ClusterRpcProxy(CONFIG) as rpc:
        account = rpc.userService.get_account(request.args.get('account_id'))
    return Response(
        GetAccountSchema().dumps(account),
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(parse_args.port), debug=True)
