from dataclasses import dataclass

import redis
from redis.commands.search.field import (
    VectorField, TagField, NumericField, TextField
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


@dataclass
class EmbeddingInfo():
    key: str = ''
    tag: str = ''
    ntokens: int = 0
    text: str = ''
    embedding: np.ndarray = None


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
            NumericField('ntokens'),
            TextField('text'),
        ]
        self.conn.ft(self.index).create_index(schema)

    def info(self):
        self.conn.ft(self.index).info()

    def drop_index(self):
        self.conn.ft(self.index).dropindex(delete_documents=True)

    def put(self, embedding: EmbeddingInfo):
        if embedding.key == '':
            raise ValueError('Error: embedding has no key')

        self.conn.hset(embedding.key, mapping={
            'embedding': embedding.embedding.tobytes(),
            'tag': embedding.tag,
            'ntokens': embedding.ntokens,
            'text': embedding.text,
        })

    def getdata(self, key, field):
        return self.conn.hget(key, field)

    def get_tag(self, key):
        return self.getdata(key, 'tag').decode('utf-8')

    def get_text(self, key):
        return self.getdata(key, 'text').decode('utf-8')

    def get_ntokens(self, key):
        return int(self.getdata(key, 'ntokens'))

    def get_embedding(self, key):
        data = self.getdata(key, 'embedding')
        return np.frombuffer(data, dtype=np.float32)

    def get(self, key):
        return EmbeddingInfo(
            key=key,
            tag=self.get_tag(key),
            text=self.get_text(key),
            ntokens=self.get_ntokens(key),
            embedding=self.get_embedding(key),
        )

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
            ret.append({
                'key': r.id,
                'vector_score': r.vector_score,
                'tag': r.tag,
                'text': r.text,
            })
        return ret
