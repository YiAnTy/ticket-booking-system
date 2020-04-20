from nameko.rpc import rpc

class TicketService(object):
    name = "ticketService"

    @rpc
    def generate_tickets(self):
        return None

    @rpc
    def reserve_ticket(self):
        return None