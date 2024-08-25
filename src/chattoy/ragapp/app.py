from typing import List
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from .config import Config


class Documents:
    def __init__(self):
        self.config = Config()

    def add(self, path: str):
        # read document
        if Path(path).is_file():
            reader = SimpleDirectoryReader(input_files=[path])
        else:
            reader = SimpleDirectoryReader(path)

        docs = reader.load_data()
        nodes = self.config.text_splitter.get_nodes_from_documents(docs)

        # create index from added documents
        index = VectorStoreIndex(nodes, storage_context=self.config.storage_context)
        retriever = index.as_query_engine(streaming=True)

        # save to database
        # TODO

        while True:
            r = retriever.query(input(">>> "))
            r.print_response_stream()
            print()

    def ls(self) -> List[str]:
        pass

    def rm(self, id: str):
        pass

    def search(self, prompt: str) -> List[str]:
        index = VectorStoreIndex.from_vector_store(self.config.vector_store)

        retriever = index.as_retriever()
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
