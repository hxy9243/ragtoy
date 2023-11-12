from typing import List
import logging
import requests
from urllib import parse

from .models import (
    DocumentRequest,
    DocumentResponse,
    ConversationRequest,
    ConversationResponse,
    MessageRequest,
    MessageResponse,
)


class Client:
    def __init__(self, server_addr):
        self.server_addr = server_addr

    def post_document(self, name, doctype, document) -> DocumentResponse:
        doc = DocumentRequest(name=name, doctype=doctype, document=document)
        r = requests.post(
            parse.urljoin(self.server_addr, "/api/documents"),
            headers={"content-type": "application/json"},
            json=doc.data(),
        )
        logging.debug(f'getting API response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error creating new document <{r.status_code}>: "{r.text}"'
            )

        return DocumentResponse.parse(r.json())

    def get_document(self, docid) -> DocumentResponse:
        r = requests.get(
            parse.urljoin(self.server_addr, f"/api/documents/{docid}"),
        )
        logging.debug(f'getting API response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error querying get document {docid} <{r.status_code}>: "{r.text}"'
            )
        return DocumentResponse.parse(r.json())

    def get_documents(self) -> List[DocumentResponse]:
        r = requests.get(
            parse.urljoin(self.server_addr, "/api/documents"),
        )
        logging.debug(f'getting API response <{r.status_code}>: "{r.text}"')
        docs = []
        for doc in r.json():
            docs.append(DocumentResponse.parse(doc))
        return docs

    def delete_document(self, docid) -> DocumentResponse:
        r = requests.delete(
            parse.urljoin(self.server_addr, f"/api/documents/{docid}"),
        )
        logging.debug(f'getting delete API response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error deleting document {docid} <{r.status_code}>: "{r.text}"'
            )

        return DocumentResponse.parse(r)

    def add_conversation(self, req: ConversationRequest) -> ConversationResponse:
        r = requests.post(
            parse.urljoin(self.server_addr, f"/api/conversations"),
            json=req.json(),
        )
        logging.debug(f'getting add API response <{r.status_code}>: "{r.text}"')
        return ConversationResponse.parse(r.json())

    def get_conversation(self, convid: str) -> ConversationResponse:
        r = requests.get(
            parse.urljoin(self.server_addr, f"/api/conversations/{convid}"),
        )
        logging.debug(f'getting get API response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error getting conversations <{r.status_code}>: "{r.text}"'
            )
        return ConversationResponse.parse(r.json())

    def get_conversations(self) -> List[ConversationResponse]:
        r = requests.get(
            parse.urljoin(self.server_addr, "/api/conversations"),
        )
        logging.debug(f'getting get response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error getting conversations <{r.status_code}>: "{r.text}"'
            )

        convs = []
        for conv in r.json():
            convs.append(ConversationResponse.parse(conv))

        return convs

    def delete_conversation(self, convid: str) -> ConversationResponse:
        r = requests.delete(
            parse.urljoin(self.server_addr, f"/api/conversations/{convid}"),
        )
        logging.debug(f'getting delete response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error getting conversations <{r.status_code}>: "{r.text}"'
            )
        return ConversationResponse.parse(r.json())

    def add_message(self, convid: str, msg: MessageRequest) -> List[MessageResponse]:
        r = requests.post(
            parse.urljoin(self.server_addr, f"/api/conversations/{convid}/messages"),
            json=msg.data(),
        )
        logging.debug(f'adding new message response <{r.status_code}>: "{r.text}"')
        if r.status_code >= 400:
            raise Exception(
                f'Error getting conversations <{r.status_code}>: "{r.text}"'
            )
        msgs = []
        for msg in r.json():
            msgs.append(MessageResponse.parse(msg))

        return msgs
