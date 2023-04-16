from wiki_qa import get_text, text_preproc, split_chunks, group_chunks

from spacy.lang.en import English

from tqdm import tqdm

WIKI_PAGE = 'wiki/Alan_Turing'

MAX_TOKENS = 256

TOKEN_MODEL = 'cl100k_base'


def get_naive_chunks(text):
    text = text_preproc(text)

    chunks = split_chunks(text, max_tokens=MAX_TOKENS)

    for c in chunks:
        print('-' * 40)
        print(c)
        print('-' * 40)


def spacy_paragraphs(text):
    chunks = []
    existing_ps = []

    # text = text_preproc(text)
    nlp = English()
    nlp.add_pipe('sentencizer')

    paragraphs = text.split('\n\n')
    for i, p in enumerate(tqdm(paragraphs)):
        existing_ps.append(p)

        if len(p) < 32 and i < len(paragraphs)-1:
            continue

        cs = spacy_chunks(nlp, '\n'.join(existing_ps))
        chunks += cs
        existing_ps = []

    return chunks


def spacy_chunks(pipeline, text):
    doc = pipeline(text)
    sentences = [sent.text for sent in doc.sents]

    return group_chunks(sentences, max_tokens=MAX_TOKENS)


if __name__ == '__main__':
    text = get_text('Alan_Turing.txt', 'wiki/Alan_Turing')

    chunks = spacy_paragraphs(text)

    print('total chunks: ', len(chunks))

    for chunk in chunks:
        print(chunk)
