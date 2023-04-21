''' LLM class creates wrapper for creating context for LLM operations like
creating embedding, creating context, queries GPT endpoint
'''

import time
import logging

import numpy as np
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import tiktoken
import openai


TOKEN_MODEL = 'cl100k_base'

EMBEDDING_MODEL = 'text-embedding-ada-002'

COMPLETION_MODEL = 'text-davinci-003'

GPT3_EMBEDDING_SIZE = 1536

MAX_CHUNK_TOKENS = 256

MIN_PARAGRAPH_LEN = 1024

MAX_COMPLETION_TOKENS = 1024


class Preprocessor:
    '''creating chunks for documentation
    '''

    def __init__(self,
                 max_chunktokens=MAX_CHUNK_TOKENS,
                 min_paragraphlen=MIN_PARAGRAPH_LEN,
                 ):

        self.max_chunktokens = max_chunktokens
        self.min_paragraphlen = min_paragraphlen

    def _remove_empty_chars(self, serie):
        serie = serie.replace('\n', ' ')
        serie = serie.replace('\\n', ' ')
        serie = serie.replace('  ', ' ')
        serie = serie.replace('  ', ' ')

        return serie

    def get_lang(self, text):
        @Language.factory("language_detector")
        def get_lang_detector(nlp, name):
            return LanguageDetector()

        detector = spacy.load("en_core_web_sm")
        detector.add_pipe('language_detector', last=True)
        return detector(text[:64])._.language['language']

    def get_spacy_model(self, lang):
        if lang == 'zh-cn' or lang == 'zh-tw':
            from spacy.lang.zh import Chinese
            return Chinese()
        elif lang == 'en':
            from spacy.lang.en import English
            return English()
        elif lang == 'jp':
            from spacy.lang.ja import Japanese
            return Japanese()
        elif lang == 'ko':
            from spacy.lang.ko import Korean
            return Korean()
        elif lang == 'es':
            from spacy.lang.es import Spanish
            return Spanish()
        elif lang == 'de':
            from spacy.lang.de import German
            return German()
        elif lang == 'fr':
            from spacy.lang.fr import French
            return French()
        else:
            print('loading english')
            from spacy.lang.en import English
            return English()

    def _create_chunks(self, text):
        nlp = self.get_spacy_model(lang=self.get_lang(text))
        nlp.add_pipe('sentencizer')

        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]

        tokenizer = tiktoken.get_encoding(TOKEN_MODEL)

        # Get the number of tokens for each sentence
        n_tokens = [len(tokenizer.encode(' ' + sentence))
                    for sentence in sentences]

        chunks = []
        tokens_so_far = 0
        chunk = []

        for sentence, n in zip(sentences, n_tokens):
            if n + tokens_so_far >= self.max_chunktokens and chunk:
                chunks.append((' '.join(chunk), tokens_so_far))
                tokens_so_far = 0
                chunk = []

            chunk.append(sentence)
            tokens_so_far += n

        if chunk:
            chunks.append((' '.join(chunk), tokens_so_far))

        return chunks

    def chunkify(self, text):
        chunks = []
        existing_ps = []

        paragraphs = text.split('\n\n')

        for i, p in enumerate(paragraphs):
            existing_ps.append(p)

            # do not split if paragraph is too small
            if len(p) < self.min_paragraphlen and i < len(paragraphs)-1:
                continue

            chunktext = '\n'.join(existing_ps)
            chunktext = self._remove_empty_chars(chunktext)

            cs = self._create_chunks(chunktext)
            chunks += cs
            existing_ps = []

        return chunks


class LLM:
    RETRIES = 10

    def __init__(self, api_key):
        openai.api_key = api_key

    def create_embedding(self, text):
        for _ in range(LLM.RETRIES):
            try:
                logging.info('Calling openAI embedding API...')
                embedding = openai.Embedding.create(
                    input=[text], model=EMBEDDING_MODEL,
                )['data'][0]['embedding']
            except openai.error.RateLimitError:
                logging.warn('Error: hit rate limiter, retrying...')
                time.sleep(10)
            except Exception:
                raise Exception
            else:
                break

        logging.debug(f'Returning API embedding size of {len(embedding)}')
        return np.array(embedding).astype(np.float32)

    def create_completion(self, prompt,
                          model=COMPLETION_MODEL,
                          max_tokens=MAX_COMPLETION_TOKENS,
                          temperature=0,
                          frequency_penalty=0,
                          presence_penalty=0,
                          ):
        for _ in range(LLM.RETRIES):
            try:
                logging.info('Calling openAI embedding API...')
                response = openai.Completion.create(
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=None,
                    model=model,
                )
            except openai.error.RateLimitError:
                logging.warn('Error: hit rate limiter, retrying...')
                time.sleep(10)
            except Exception:
                raise Exception
            else:
                break

        return response['choices'][0]['text'].strip()
