from typing import List
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

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
        retriever = index.as_chat_engine(streaming=True, similarity_top_k=3)

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
