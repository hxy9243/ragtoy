import pytest

import numpy as np

from vector import VectorSearch

EMBEDDING_SIZE = 8


@pytest.fixture
def vector_search():
    return VectorSearch('testidx', embedding_size=EMBEDDING_SIZE)


def test_initvector(vector_search):
    vector_search.create_index()

    for i in range(10):
        data = np.random.random(EMBEDDING_SIZE). \
            astype(np.float32).tobytes()

        vector_search.put(i, data, 'text-'+str(i))

def test_cleanup(vector_search):
    vector_search.drop_index()

