from nameko.extensions import DependencyProvider
import redis
from ticketservice import config
from ticketservice.exceptions import NotFound


REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:
    """
    Product storage

    A very simple example of a custom Nameko dependency. Simplified
    implementation of products database based on Redis key value store.
    Handling the product ID increments or keeping sorted sets of product
    names for ordering the products is out of the scope of this example.

    """

    NotFound = NotFound

    def __init__(self, client):
        self.client = client

    def _format_key(self, ticket_id):
        return 'tickets:{}'.format(ticket_id)

    def _from_hash(self, document):
        return {
            'id': document[b'id'].decode('utf-8'),
            'title': document[b'title'].decode('utf-8'),
        }

    def get(self, ticket_id):
        product = self.client.hgetall(self._format_key(ticket_id))
        if not product:
            raise NotFound('Ticket ID {} does not exist'.format(ticket_id))
        else:
            return self._from_hash(product)

    def list(self):
        keys = self.client.keys(self._format_key('*'))
        for key in keys:
            yield self._from_hash(self.client.hgetall(key))

    def create(self, ticket):
        self.client.hmset(
            self._format_key(ticket['id']),
            ticket)

    def decrement_stock(self, product_id, amount):
        return self.client.hincrby(
            self._format_key(product_id), 'in_stock', -amount)


class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url('redis://user:test123@localhost:6379/11')

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)


class RedisClient(object):
    """
    redis client
    """
    redis_client = {}

    @staticmethod
    def reload_redis(host, port, select_db):
        """
        function: reload redis object
        """
        return redis.StrictRedis(
            host=host,
            port=port,
            db=select_db,
            password="",
            decode_responses=True)

    @classmethod
    def get_redis(cls, redis_name, host, port, select_db):
        """
        function: get redis client
        """
        if redis_name not in cls.redis_client:
            cls.redis_client[redis_name] = cls.reload_redis(
                host, port, select_db)
        return cls.redis_client.get(redis_name)
