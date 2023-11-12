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
        return r.parse(r.json())

    def get_conversations(self):
        pass

    def get_conversation(self, convid):
        pass

    def delete_conversation(self, convid):
        pass

    def add_message(self, convid, msg):
        pass

    def get_messages(self, convid):
        pass
