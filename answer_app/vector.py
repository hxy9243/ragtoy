import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query

import numpy as np

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
            'embedding': embedding.tobytes(),
            'text_id': text_id,
        })
        pass

    def get(self, key, field):
        return self.conn.hget(key, field)

    def get_textid(self, key):
        return self.get(key, 'text_id').decode('utf-8')

    def get_embedding(self, key):
        data = self.get(key, 'embedding')
        return np.frombuffer(data, dtype=np.float32)

    def search(self, vector, max=5):
        querystr = f'*=>[KNN {max} @embedding $vector AS vector_score]'
        query = Query(querystr).return_fields(
            'vector_score', 'embedding', 'text_id',
        ).sort_by('vector_score').dialect(2)

        results = self.conn.ft(self.index).search(
            query,
            query_params={'vector': vector.tobytes()},
        )

        ret = []
        for r in results.docs:
            print(r.id)
            ret.append({
                'key': r.id,
                'vector_score': r.vector_score,
                'text_id': r.text_id,
            })
        return ret
