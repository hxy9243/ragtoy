from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, Document, Chunk


class DB:
    def __init__(self, db: str):
        self.engine = create_engine(db)

    def get_session(self) -> Session:
        return Session(self.engine)


class DocumentService:
    def __init__(self, db: DB):
        self.db = db
        Base.metadata.create_all(self.db.engine)

    def add(self, doc: Dict, chunks: List[Dict]) -> Document:
        d = Document(
            id=doc['id'],
            name=doc['name'],
            path=doc['path'],
            hash=doc['hash'],
            type=doc['hash'],
            created_time=doc['created_time'],
        )
        cs = [
            Chunk(
                id=chunk['id'],
                hash=chunk['hash'],
            ) for chunk in chunks
        ]

        d.chunks = cs

        with self.db.get_session() as session:
            session.add(d)
            # session.add_all(cs)

            session.commit()
