from typing import List
import logging
import requests
from urllib import parse

from .models import (
    DocumentRequest, DocumentResponse,
    ConversationRequest, ConversationResponse,
    MessageRequest, MessageResponse,
)


class Client:

    def __init__(self, server_addr):
        self.server_addr = server_addr

    def add_document(self, doc: DocumentRequest) -> DocumentResponse:
        r = requests.post(
            parse.urljoin(self.server_addr, '/api/documents'),
            headers={'content-type': 'application/json'},
            data=doc.data(),
        )
        logging.debug('getting API response:', r.status_code, r.text)

        return DocumentResponse.parse(r.json())

    def get_document(self, docid) -> DocumentResponse:
        r = requests.get(
            parse.urljoin(self.server_addr, f'/api/documents/{docid}'),
        )
        logging.debug(f'getting API response <{r.status_code}>: "{r.text}"')
        return DocumentResponse.parse(r.json())

    def get_documents(self) -> List[DocumentResponse]:
        r = requests.get(
            parse.urljoin(self.server_addr, '/api/documents'),
        )
        logging.debug(f'getting API response <{r.status_code}>: "{r.text}"')
        docs = []
        for doc in r.json():
            docs.append(DocumentResponse.parse(doc))
        return docs

    def delete_documents(self, docid):
        r = requests.delete(
            parse.urljoin(self.server_addr, f'/api/documents/{docid}'),
        )
        return

    def add_conversation(self, docid, conv):

        pass

    def get_conversations(self, docid):

        pass

    def get_conversation(self, convid):

        pass

    def delete_conversation(self, convid):

        pass

    def add_message(self, convid, msg):

        pass

    def get_messages(self, convid):

        pass
