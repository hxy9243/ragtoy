from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import chromadb
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


@dataclass
class Config:
    db = None
    vector = None

    def __init__(self):
        load_dotenv()

        Path("db").mkdir(exist_ok=True)

        chroma_db = chromadb.PersistentClient("db/chattoy.chroma")
        chroma_coll = chroma_db.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})

        self.db_url = "sqlite:///db/ragtoy.db"

        self.vector_store = ChromaVectorStore(chroma_collection=chroma_coll)
        self.text_splitter = SentenceSplitter.from_defaults(
            include_metadata=True, chunk_size=1024, chunk_overlap=20,
        )
        self._setup_llama_index()

    def _setup_llama_index(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()

        """ Settings.llm = OpenAI(
            # model="llama3-8b",
            api_key=os.environ["API_KEY"],
            api_base=os.environ["API_URL"],
            default_headers={"Authorization": "Basic " + os.environ["API_KEY"]},
            additional_kwargs={"model": "llama3-70b"},
        ) """
        Settings.llm = OpenAI()
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
