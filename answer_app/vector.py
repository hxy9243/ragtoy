import redis
from redis.commands.search.field import (
    VectorField, TagField, TextField
)
from redis.commands.search.query import Query

import numpy as np

GPT3_EMBEDDING_SIZE = 2048


class VectorIndices:
    def __init__(self,
                 host='localhost',
                 port=6379):
        self.conn = redis.Redis(host=host, port=port)

    def list(self):
        return self.conn.execute_command('ft._list')

    def get(self, idx):
        return VectorIndex(self.conn, idx)

    def create(self, idx, embedding_size=GPT3_EMBEDDING_SIZE):
        vi = VectorIndex(self.conn, idx, embedding_size)
        vi.create_index(embedding_size)

        return vi


class VectorIndex:
    def __init__(self,
                 conn,
                 index,
                 ):
        self.conn = conn
        self.index = index

    def create_index(self, embedding_size=GPT3_EMBEDDING_SIZE):
        schema = [
            VectorField('embedding',
                        'hnsw',
                        {
                            "TYPE": 'FLOAT32',
                            "DIM": embedding_size,
                            "DISTANCE_METRIC": 'cosine',
                        }),
            TagField('tag'),
            TextField('text'),
        ]
        self.conn.ft(self.index).create_index(schema)

    def info(self):
        self.conn.ft(self.index).info()

    def drop_index(self):
        self.conn.ft(self.index).dropindex(delete_documents=True)

    def put(self, key, tag, text, embedding):
        self.conn.hset(key, mapping={
            'embedding': embedding.tobytes(),
            'tag': tag,
            'text': text,
        })
        pass

    def get(self, key, field):
        return self.conn.hget(key, field)

    def get_tag(self, key):
        return self.get(key, 'tag').decode('utf-8')

    def get_text(self, key):
        return self.get(key, 'text').decode('utf-8')

    def get_embedding(self, key):
        data = self.get(key, 'embedding')
        return np.frombuffer(data, dtype=np.float32)

    def search(self, vector, max=5):
        querystr = f'*=>[KNN {max} @embedding $vector AS vector_score]'
        query = Query(querystr).return_fields(
            'vector_score', 'embedding', 'tag', 'text',
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
                'tag': r.tag,
                'text': r.text,
            })
        return ret
