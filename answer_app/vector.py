import redis
from redis.commands.search.fields import VectorField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis import Connection


GPT3_EMBEDDING_SIZE = 2048


class VectorSearch:

    def __init__(self,
                 host='localhost',
                 port=6379):
        self.conn = redis.Redis(host=host, port=port)

    def create(self, key):
        schema = [
            VectorField('$.embedding',
                        'hnsw',
                        {
                            "TYPE": 'FLOAT32',
                            "DIM": GPT3_EMBEDDING_SIZE,
                            "DISTANCE_METRIC": 'cosine',
                        },
                        as_name='embedding',
                        ),
            TagField('$.text_id', as_name='text_id')
        ]
        idx_def: IndexDefinition = IndexDefinition(
            index_type=IndexType.JSON, prefix=['key:'])
        self.conn.ft('idx').create_index(schema, definition=idx_def)
        pipe: Connection = self.conn.pipeline()

        for id, vec in self.image_dict.items():
            pipe.json().set(
                f'key:{id}', '$',
                {
                    'text_id': id, 'embedding': vec
                },
            )
        pipe.execute()

    def put(self, key, vector, metadata):

        pass

    def search(self, key, vecotr, max=5):

        pass
