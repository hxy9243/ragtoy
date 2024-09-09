from typing import List
from pathlib import Path
import logging

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode

from .config import Config
from .database import DocumentService

class Documents:
    def __init__(self):
        self.config = Config()
        self.docsvc = DocumentService(db_url=self.config.db_url)

    def add(self, path: str):
        # read document and preprocess (chunking), and saves info
        if Path(path).is_file():
            reader = SimpleDirectoryReader(input_files=[path])
        else:
            reader = SimpleDirectoryReader(path)

        docs = reader.load_data()
        for doc in docs:
            existing = self.docsvc.get_doc(hash=doc.hash)
            if existing:
                logging.warn(f"Skipping existing document: {existing.path}")
                continue

            nodes = self.config.text_splitter.get_nodes_from_documents([doc])

            # saves document
            self.docsvc.add_doc(
                doc={**doc.to_dict(), 'hash': doc.hash},
                chunks=[n.to_dict() for n in nodes],
            )

            for node in nodes:
                print(node.node_id)
                print(node.get_type())
                print(node.hash)
                print(node.extra_info)
                print()

            # create index from added documents
            index = VectorStoreIndex.from_vector_store(
                vector_store=self.config.vector_store,
                show_progress=True,
            )
            index.insert_nodes(nodes)

    def ls(self) -> List[str]:
        pass

    def rm(self, id: str):
        pass

    def chat(self):
        # create index from added documents
        index = VectorStoreIndex.from_vector_store(vector_store=self.config.vector_store)
        retriever = index.as_chat_engine(
            streaming=True,
            similarity_top_k=3,
            chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        )

        while True:
            r = retriever.stream_chat(input("question > "))
            r.print_response_stream()
            print('\n' + '=' * 40)
            print("Sources:")
            for i, n in enumerate(r.source_nodes):
                if i != 0:
                    print('-' * 20)
                print(n)
            print('=' * 40)

    def search(self, prompt: str, top_k: int=3) -> List[str]:
        index = VectorStoreIndex.from_vector_store(self.config.vector_store)

        retriever = index.as_retriever(similarity_top_k=top_k)
        return retriever.retrieve(prompt)

    def related(self, docid: str, limit=5) -> List[str]:
        pass


class Messages:
    def __init__(self) -> None:
        pass

    def query(self, prompt: str) -> str:
        pass

    def get(self) -> List[str]:
        pass
