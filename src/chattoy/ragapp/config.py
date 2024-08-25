from dataclasses import dataclass

import sqlite3

from dotenv import load_dotenv
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


@dataclass
class Config:
    db = None
    vector = None

    def __init__(self):
        load_dotenv()

        self.db = sqlite3.connect("db/chattoy.db")
        chroma_db = chromadb.PersistentClient("db/chattoy.chroma")
        chroma_coll = chroma_db.get_or_create_collection("rag")

        self.vector_store = ChromaVectorStore(chroma_collection=chroma_coll)

        self._setup_llama_index()

    def _setup_llama_index(self):
        Settings.llm = OpenAI(model="gpt-3.5-turbo")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
