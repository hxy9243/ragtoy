import logging

from chattoy.client import Client


def main():
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    client = Client('http://localhost:5000')

    docs = client.get_documents()

    for doc in docs:
        print(doc)


if __name__ == '__main__':
    main()
