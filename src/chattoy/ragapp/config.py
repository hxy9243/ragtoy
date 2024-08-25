from dataclasses import dataclass

from pathlib import Path
import sqlite3

from dotenv import load_dotenv
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, StorageContext

# from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.node_parser import SentenceSplitter

@dataclass
class Config:
    db = None
    vector = None

    def __init__(self):
        load_dotenv()

        Path("db").mkdir(exist_ok=True)

        self.db = sqlite3.connect("db/chattoy.db")
        chroma_db = chromadb.PersistentClient("db/chattoy.chroma")
        chroma_coll = chroma_db.get_or_create_collection("rag", metadata={"hnsw:space": "cosine"})

        self.vector_store = ChromaVectorStore(chroma_collection=chroma_coll)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.text_splitter = SentenceSplitter.from_defaults(
            include_metadata=True, chunk_size=1024, chunk_overlap=20,
        )
        self._setup_llama_index()

    def _setup_llama_index(self):
        Settings.llm = OpenAI(model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

