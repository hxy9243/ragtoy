from typing import Dict, List
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, Document, Chunk


class DB:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_session(self) -> Session:
        return Session(self.engine)


class DocumentService:
    def __init__(self, db_url: str):
        self.db = DB(db_url)
        Base.metadata.create_all(self.db.engine)

    def dict_to_document(self, doc: Dict) -> Document:
        return Document(
            id=doc['id_'],
            name=doc['metadata']['file_name'],
            path=doc['metadata']['file_path'],
            hash=doc['hash'],
            type=doc['metadata']['file_type'],
            text=doc['text'],
            creation_date=datetime.strptime(doc['metadata']['creation_date'], '%Y-%m-%d'),
        )

    def dict_to_chunk(self, node: Dict, docid: str) -> Chunk:
        return Chunk(id=node['id_'], docid=docid)

    def add_doc(self, doc: Dict, chunks: List[Dict]) -> Document:
        d = self.dict_to_document(doc)
        d.chunks = [self.dict_to_chunk(chunk, docid=doc['id_']) for chunk in chunks]

        with self.db.get_session() as session:
            session.add(d)
            session.commit()

    def get_doc(self, **kwargs) -> Document:
        with self.db.get_session() as session:
            return session.query(Document).filter_by(**kwargs).first()
