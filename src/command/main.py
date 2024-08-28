from typing import List

import sys
import logging

import click

from ragtoy.config import Config
from ragtoy.app import Documents

logging.basicConfig(level=logging.WARN, handlers=[logging.StreamHandler(sys.stdout)])


@click.command(help="Ask questions based on all the documents in the DB")
def chat():
    docs = Documents()

    logging.debug(f"Interactively asking questions")
    docs.chat()


@click.group(help="Document related operations")
def document():
    pass


@click.command(help="Add a new document or a directory defined by path")
@click.argument("path")
def add(path: str):
    logging.debug(f"Adding a new path {path}")

    Documents().add(path)


@click.command(help="List the documents")
@click.argument("docid", default=None)
def ls(docid: str | None):
    logging.debug(f"Listing documents")


@click.command(help="Remove a document")
@click.argument("docid")
def rm(docid: str):
    logging.debug(f"Remove a document {docid}")


@click.command(help="Search the most related documents based on prompt")
@click.argument("prompt")
def search(prompt: str):
    logging.debug(f"Search a document based on prompt: {prompt}")

    nodes = Documents().search(prompt)
    for n in nodes:
        text = n.text[:min(len(n.text), 128)]
        print(f"{n.metadata['file_path']} \nText: {text}...\nScore: {n.score}")
        print("-" * 40)


@click.command(help="")
@click.argument("docid")
def related(docid: str):
    logging.debug(f"find the most related documents with: {docid}")


document.add_command(add)
document.add_command(ls)
document.add_command(rm)
document.add_command(search)
document.add_command(related)


@click.group()
def main():
    pass


main.add_command(document)
main.add_command(chat)

if __name__ == "__main__":
    main()
