import pytest
import os

from datetime import datetime

from .database import DB, DocumentService


@pytest.fixture
def db():
    DB_PATH = '/tmp/test.db'
    yield DB(f'sqlite:///{DB_PATH}')

    os.remove(DB_PATH)


def test_database(db):
    svc = DocumentService(db)
    svc.add(
        doc={
            'id': '1',
            'name': 'example.txt',
            'path': '/home/kevinh/example.txt',
            'hash': '12345',
            'type': 'text',
            'created_time': datetime.now(),
        },
        chunks=[
            {
                'id': '1',
                'hash': '12345',
            },
        ],
    )


