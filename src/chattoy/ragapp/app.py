from typing import List

from .config import Config

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex

class Documents:
    def __init__(self, config: Config):
        self.config = config


    def add(self, path: str):
        # chunkfy document

        # create embeddings

        # save embedding

        # save document

        pass

    def ls(self) -> List[str]:
        pass

    def rm(self, id: str):
        pass

    def search(self, prompt: str) -> List[str]:
        pass

    def related(self, docid: str, limit=5) -> List[str]:
        pass




class Messages:
    def __init__(self) -> None:
        pass

    def query(self, prompt: str) -> str:
        pass

    def get(self) -> List[str]:
        pass
