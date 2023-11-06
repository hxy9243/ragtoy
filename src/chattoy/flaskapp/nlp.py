''' LLM class creates wrapper for Langchain operations
'''

from typing import List, Tuple

import numpy as np
import tiktoken
import langchain
from langchain.llms import OpenAI
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


TOKEN_MODEL = 'cl100k_base'

GPT3_EMBEDDING_SIZE = 1536

MAX_CHUNK_SIZE = 256

CHUNK_OVERLAP = 40

MAX_COMPLETION_TOKENS = 1024


class LLM:

    def __init__(self, openai_api_key: str):
        self.embedding = self.get_embedding(
            openai_api_key=openai_api_key)
        self.llm = self.get_llm(openai_api_key=openai_api_key)

    def get_llm(self, *args, **kwargs) -> LLM:
        return OpenAI(openai_api_key=kwargs['openai_api_key'])

    def get_embedding(self, *args, **kwargs) -> Embeddings:
        return langchain.embeddings.OpenAIEmbeddings(
            openai_api_key=kwargs['openai_api_key'])

    def chunkify(self, text,
                 chunk_size=MAX_CHUNK_SIZE,
                 chunk_overlap=CHUNK_OVERLAP,
                 *args, **kwargs,
                 ) -> List[Tuple[int, str]]:
        ''' chunkify returns a list of tuple of each chunk and its token size.
        '''
        splitted = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            *args, **kwargs,
        ).split_text(text)

        chunks = []

        tokenizer = tiktoken.get_encoding(TOKEN_MODEL)

        for paragraph in splitted:
            n_tokens = tokenizer.encode(paragraph)
            chunks.append((paragraph, len(n_tokens)))

        return chunks

    def create_embedding(self,
                         text: str):
        ''' create embedding for the input text
        '''
        embedding = self.embedding.embed_query(text)

        return np.array(embedding).astype(np.float32)

    def create_completion(self, prompt) -> str:
        ''' create LLM prompt completion for the input prompt
        '''
        return self.llm(prompt)
