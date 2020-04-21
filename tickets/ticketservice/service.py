from nameko.events import event_handler
from nameko.rpc import rpc

from ticketservice import dependencies, schemas

class TicketService(object):

    name = "ticketService"

    storage = dependencies.Storage()

    @rpc
    def get(self, ticket_id):
        ticket = self.storage.get(ticket_id)
        return schemas.Ticket().dump(ticket)

    @rpc
    def list(self):
        tickets = self.storage.list()
        return schemas.Ticket(many=True).dump(tickets)

    @rpc
    def create(self, ticket):
        ticket = schemas.Ticket().load(ticket)
        self.storage.create(ticket)

    @event_handler('orders', 'order_created')
    def handle_order_created(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])