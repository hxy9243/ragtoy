import pytest

import numpy as np


from vector import VectorSearch

EMBEDDING_SIZE = 8


def _create_random_vectors():
    vectors = []
    for i in range(10):
        vectors.append(
            np.random.random(EMBEDDING_SIZE).astype(np.float32)
        )
    return vectors


def cosine(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


@pytest.fixture
def vector_search():
    return VectorSearch('testidx', embedding_size=EMBEDDING_SIZE)


def test_initvector(vector_search):
    vector_search.create_index()


def test_putvector(vector_search):
    vectors = _create_random_vectors()

    for i in range(10):
        data = vectors[i]
        vector_search.put(i, data, 'text-'+str(i))

    # test get textid
    textid = vector_search.get_textid(1)
    assert textid == 'text-1', \
        'ValueError: expecting text-1, getting ' + textid

    # test get embedding
    for i in range(10):
        embedding = vector_search.get_embedding(i)

        assert np.array_equal(embedding, vectors[i]), \
            f'Error, getting unexpected embedding value at index {i}'


def test_searchvector(vector_search):
    search_vector = np.random.random(EMBEDDING_SIZE).astype(np.float32)

    results = vector_search.search(search_vector, max=10)
    scores = []

    for r in results:
        print(r)
        embedding = vector_search.get_embedding(r['key'])
        score = cosine(search_vector, embedding)
        scores.append(score)

    # embedding is sorted by highest score
    scores.reverse()
    assert scores == sorted(scores), 'Search result not sorted'


def test_cleanup(vector_search):
    vector_search.drop_index()

