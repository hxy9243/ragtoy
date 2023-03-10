import os
import sys
import csv

from dotenv import load_dotenv
import tiktoken
import openai


TOKEN_MODEL = 'cl100k_base'

EMBEDDING_MODEL = 'text-embedding-ada-002'

MAX_TOKENS = 256


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
            chunks .append(
                '. '.join(chunk) + '.',
            )
            tokens_so_far = 0
            chunk = []

        tokens_so_far += n
        chunk.append(sentence)

    return chunks


def create_embeddings(chunks):
    embedding_data = []
    for _, chunk in chunks:
        embedding = openai.Embedding.create(
            input=[chunk], model=EMBEDDING_MODEL)['data'][0]['embedding']
        embedding_data.append((chunk, embedding))

    return embedding_data


def get_embeddings(csvfile, chunks):
    if os.path.exists(csvfile):
        with open(csvfile, 'rw') as f:
            embedding_data = []

            reader = csv.reader(f, delimiter=',')
            for r in reader:
                embedding_data.append(r)
    else:
        embedding_data = create_embeddings(chunks)

    return embedding_data


def main():
    if len(sys.argv) == 1:
        print('Usage: app <text_file>')
        os.exit(1)

    with open(sys.argv[1], 'r') as f:
        text = f.read()

    text = text_preproc(text)
    chunks = split_chunks(text)

    for i, c in enumerate(chunks):
        print(f'----- {i} -----')
        print(c)

    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    embedding_data = create_emebeddings(chunks)


if __name__ == '__main__':
    main()
