import logging
import hashlib
import uuid
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import Column, String, Text, Integer, DateTime

from models.base import Base, engine


class Document(Base):
    __tablename__ = 'documents'
    docid = Column('id', String(16), primary_key=True)
    name = Column('name', String(128), unique=True, nullable=False)
    doctype = Column('type', String(16), default='text')
    hash = Column('hash', String(64))
    body = Column('body', Text)
    ntokens = Column('ntokens', Integer)
    created = Column('created_time', DateTime)

    # conversations = relationship(
    #     'Conversation',
    #     cascade="all, delete-orphan",
    #     back_populates='doc',
    # )

    def __repr__(self):
        return f'<Document {self.docid}>'

    def data(self):
        return {
            'id': self.docid,
            'name': self.name,
            'body': self.body,
            'type': self.doctype,
        }


class DocumentsApi:
    def get(self):
        session = Session(engine)

        docs = session.execute(
            select(Document).order_by(Document.created),
        ).scalars().all()

        results = []
        for doc in docs:
            results.append(doc.data())

        return results

    def _get_hash(self, body):
        return hashlib.md5(body.encode('utf-8')).hexdigest()

    def _get_existing(self, session, body):
        existing = session.execute(
            select(Document).filter(
                Document.hash == self._get_hash(body))
        ).scalars().all()
        return existing

    # def _create_embedding(self, docid, body):
    #     vectoridx = vectorindices.create(docid)

    #     chunks = Preprocessor().chunkify(body)
    #     ntokens = 0
    #     for i, chunk in enumerate(chunks):
    #         body, ntoken = chunk

    #         logging.info(f'creating #{i+1}/{len(chunks)} for doc {docid} ' +
    #                      f'{ntoken} tokens...')
    #         embedding = llm.create_embedding(body)
    #         ntokens += ntoken

    #         vectoridx.put(EmbeddingInfo(
    #             key=docid + ':' + str(i),
    #             text=body,
    #             tag=docid,
    #             ntokens=ntoken,
    #             embedding=embedding,
    #         ))

    #     return ntokens

    def post(self,
             name,
             document,
             doctype='text'):

        session = Session(engine)

        # check if the text is already uploaded, based on hash
        existing = self._get_existing(session, document)
        if len(existing) != 0:
            return []

        docid = str(uuid.uuid4())

        # create embedding for the document and saves in the vector db
        logging.info(f'creating embedding for document {docid}: {document[:32]}..')
        # ntokens = self._create_embedding(docid, document)

        newdoc = Document(
            name=name,
            docid=docid,
            doctype=doctype,
            hash=self._get_hash(document),
            body=document,
            created=datetime.now(),
            # ntokens=ntokens,
        )
        try:
            session.add(newdoc)
            session.commit()
        except Exception as exec:
            session.rollback()
            raise exec
        else:
            data = newdoc.data()

        return data

    def delete(self, docid):
        session = Session(engine)

        logging.info(f'deleting docuemnt {docid}..')

        doc = session.execute(
            select(Document).filter_by(docid=docid),
        ).scalars().one()

        logging.info(f'deleting docuemnt {doc.docid}, {doc.name}..')
        session.delete(doc)
        session.commit()
