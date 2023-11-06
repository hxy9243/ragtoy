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
            'document': self.document,
            'type': self.doctype,
        }


@dataclass
class DocumentRequest(Document):
    pass


@dataclass
class DocumentResponse(Document):

    @classmethod
    def parse(cls, data: Dict) -> 'DocumentResponse':
        return DocumentResponse(
            docid=data['id'], name=data['name'], doctype=data['type'],
            ntokens=data['ntokens'], document=data['document'],
        )


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
