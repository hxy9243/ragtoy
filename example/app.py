import os
import time

from dotenv import load_dotenv
import pandas as pd
import wikipedia
from bs4 import BeautifulSoup as BS4
import tiktoken
import openai


WIKI_PAGE = 'wiki/Alan_Turing'

TOKEN_MODEL = 'cl100k_base'

EMBEDDING_MODEL = 'text-embedding-ada-002'

MAX_TOKENS = 256


def get_text(textfile, wikipage):
    if not os.path.exists(textfile):
        wiki = wikipedia.page(wikipage)
        text = BS4(wiki.html(), 'html.parser').get_text()

        with open(textfile, 'w') as f:
            f.write(text)
        return text

    with open(textfile, 'r') as f:
        return f.read()


def text_preproc(serie: str):
    serie = serie.replace('\n', ' ')
    serie = serie.replace('\\n', ' ')
    serie = serie.replace('  ', ' ')
    serie = serie.replace('  ', ' ')

    return serie


def split_chunks(text: str, max_tokens=MAX_TOKENS):
    '''Split text into chunks of no longer than max_tokens.a
    '''

    tokenizer = tiktoken.get_encoding(TOKEN_MODEL)

    # use an approximate way to split sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence))
                for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    for n, sentence in zip(n_tokens, sentences):
        if n + tokens_so_far > max_tokens:
            chunks .append('. '.join(chunk) + '.')
            tokens_so_far = 0
            chunk = []

        tokens_so_far += n
        chunk.append(sentence)

    return chunks


def create_openai_embeddings(chunks):
    RETRIES = 10

    embedding_data = pd.DataFrame(chunks, columns=['text'])

    embeddings = []
    for chunk in chunks:
        for _ in range(RETRIES):
            try:
                embedding = openai.Embedding.create(
                    input=[chunk], model=EMBEDDING_MODEL,
                )['data'][0]['embedding']
            except openai.error.RateLimitError:
                print('Error: hit rate limiter, retrying...')
                time.sleep(10)
            except Exception:
                raise Exception
            else:
                break

        embeddings.append(embedding)

    embedding_data['embedding'] = embeddings
    return embedding_data


def get_embeddings(csvfile, chunks):
    if os.path.exists(csvfile):
        embedding_data = pd.read_csv(csvfile)
    else:
        embedding_data = create_openai_embeddings(chunks)
        embedding_data.to_csv(csvfile)

    return embedding_data


def main():
    text = get_text('turing.txt', WIKI_PAGE)

    text = text_preproc(text)
    chunks = split_chunks(text)

    for i, c in enumerate(chunks):
        print(f'----- {i} -----')
        print(c)

    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    embedding_data = get_embeddings('turing_embedding.csv', chunks)

    print(embedding_data)


if __name__ == '__main__':
    main()
