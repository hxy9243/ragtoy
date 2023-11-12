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
            "id": self.docid,
            "name": self.name,
            "type": self.doctype,
            "document": self.document,
        }


@dataclass
class DocumentRequest:
    name: str
    doctype: str
    document: str

    def data(self):
        return {
            "name": self.name,
            "type": self.doctype,
            "document": self.document,
        }


@dataclass
class DocumentResponse(Document):
    @classmethod
    def parse(cls, data: Dict) -> "DocumentResponse":
        return DocumentResponse(
            docid=data["id"],
            name=data["name"],
            doctype=data["type"],
            ntokens=data["ntokens"],
            document=data["document"],
        )

    def __repr__(self):
        if len(self.document) <= 50:
            document = self.document
        else:
            document = self.document[:50].replace("\n", " ") + "..."

        return f'[{self.docid}] {self.name} (type:({self.doctype})) "{document}"'


@dataclass
class Conversation:
    convid: str
    docid: str
    user: str
    messages: "Message"


@dataclass
class ConversationRequest(Conversation):
    user: str
    docid: str

    def json(self):
        return {
            "user": self.user,
            "docid": self.docid,
        }


@dataclass
class ConversationResponse(Conversation):
    @classmethod
    def parse(data: Dict) -> "ConversationResponse":
        return ConversationResponse(
            convid=data["convid"],
            docid=data["docid"],
            user=data["user"],
            messages=[MessageResponse.parse(msg) for msg in data["messages"]],
        )


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
    @classmethod
    def parse(cls, data: Dict) -> "MessageResponse":
        return MessageResponse(
            msgid=data["msgid"],
            convid=data["convid"],
            index=data["index"],
            context=data["context"],
            msg=data["msg"],
            ntokens=data["ntokens"],
            time=data["time"],
        )
