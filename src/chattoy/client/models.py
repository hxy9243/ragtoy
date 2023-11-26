from dataclasses import dataclass
from typing import List, Dict
import time
from datetime import datetime


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
class ConversationRequest:
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
    def parse(cls, data: Dict) -> "ConversationResponse":
        return ConversationResponse(
            convid=data["id"],
            docid=data["docid"],
            user=data["user"],
            messages=[MessageResponse.parse(msg) for msg in data["messages"]],
        )

    def dump(self, last=3):
        """pretty print conversation information"""
        print(
            f"Conversation ID: {self.convid}, Document ID: {self.docid} from user: {self.user}"
        )
        n_msgs = min(last, len(self.messages))
        for m in self.messages[-n_msgs:]:
            print(m)


@dataclass
class Message:
    msgid: str
    convid: str
    index: str
    context: str
    message: str
    ntokens: int
    msgtype: str
    time: str


@dataclass
class MessageRequest:
    text: str

    def data(self):
        return {"text": self.text}


@dataclass
class MessageResponse(Message):
    @classmethod
    def parse(cls, data: List) -> List["MessageResponse"]:
        return MessageResponse(
            msgid=data["id"],
            convid=data["convid"],
            index=data["index"],
            context=data["context"],
            message=data["message"],
            ntokens=data["ntokens"],
            time=data["time"],
            msgtype=data["msgtype"],
        )

    def __repr__(self) -> str:
        return f"[{self.time}] ({self.msgtype}) {self.message}"
