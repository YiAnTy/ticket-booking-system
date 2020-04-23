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

    @event_handler('orderService', 'order_created')
    def handle_order_created(self, payload):
        for ticket in payload['order']['order_details']:
            result = self.storage.change_status(ticket['ticket_id'], "reserved")

    @event_handler('orderService', 'order_success')
    def handle_pay_success(self, order):
        for ticket in order['order']['order_details']:
            self.storage.change_status(ticket['ticket_id'], "complete")

    @event_handler('orderService', 'order_cancel')
    def handle_refund(self, order):
        for ticket in order['order']['order_details']:
            self.storage.change_status(ticket['ticket_id'], "returned")