from dataclasses import dataclass
from typing import Dict
import time


@dataclass
class Document:
    docid: str
    name: str
    doctype: str
    document: str
    ntokens: int

    def data(self):
        return {
            'id': self.docid,
            'name': self.name,
            'type': self.doctype,
            'document': self.document,
        }


@dataclass
class DocumentRequest():
    name: str
    doctype: str
    document: str

    def data(self):
        return {
            'name': self.name,
            'type': self.doctype,
            'document': self.document,
        }


@dataclass
class DocumentResponse(Document):

    @classmethod
    def parse(cls, data: Dict) -> 'DocumentResponse':
        return DocumentResponse(
            docid=data['id'], name=data['name'], doctype=data['type'],
            ntokens=data['ntokens'], document=data['document'],
        )

    def __repr__(self):
        if len(self.document) <= 50:
            document = self.document
        else:
            document = self.document[:50].replace('\n', ' ') + '...'

        return f'[{self.docid}] {self.name} (type:({self.doctype})) "{document}"'


@dataclass
class Conversation:
    convid: str
    docid: str
    user: str


@dataclass
class ConversationRequest(Conversation):
    pass


@dataclass
class ConversationResponse(Conversation):
    pass


@dataclass
class Message:
    msgid: str
    convid: str
    index: str
    context: str
    msg: str
    ntokens: int
    time: float = time.time()


@dataclass
class MessageRequest(Message):
    pass


@dataclass
class MessageResponse(Message):
    pass
