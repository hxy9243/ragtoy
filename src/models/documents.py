import logging
import hashlib
import uuid

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text, Integer

from models.base import Base, session


class Document(Base):
    __tablename__ = 'documents'
    docid = Column('id', String(16), primary_key=True)
    name = Column('name', String(128))
    doctype = Column('type', String(16), default='text')
    hash = Column('hash', String(64))
    body = Column('body', Text)
    ntokens = Column('ntokens', Integer)

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
        docs = session.execute(session.query(Document)).scalars()
        results = []
        for doc in docs:
            results.append(doc.data())

        return results

    def _get_hash(self, body):
        return hashlib.md5(body.encode('utf-8')).hexdigest()

    def _get_existing(self, body):
        existing = session.execute(
            session.query(Document).where(
                Document.hash == self._get_hash(body)
            ),
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

        # check if the text is already uploaded, based on hash
        existing = self._get_existing(document)
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
            # ntokens=ntokens,
        )
        session.add(newdoc)
        session.commit()

        return newdoc.data()
