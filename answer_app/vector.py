import redis
from redis.commands.search.field import VectorField, TagField


GPT3_EMBEDDING_SIZE = 2048


class VectorSearch:

    def __init__(self,
                 index,
                 host='localhost',
                 port=6379,
                 embedding_size=GPT3_EMBEDDING_SIZE,
                 ):
        self.conn = redis.Redis(host=host, port=port)
        self.index = index
        self.embedding_size = embedding_size

    def create_index(self):
        schema = [
            VectorField('embedding',
                        'hnsw',
                        {
                            "TYPE": 'FLOAT32',
                            "DIM": self.embedding_size,
                            "DISTANCE_METRIC": 'cosine',
                        }),
            TagField('text_id'),
        ]
        self.conn.ft(self.index).create_index(schema)

    def drop_index(self):
        self.conn.ft(self.index).dropindex(delete_documents=True)

    def put(self, key, embedding, text_id):
        self.conn.hset(key, mapping={
            'embedding': embedding,
            'text_id': text_id,
        })
        pass

    def search(self, key, vector, max=5):

     pass
