RAG Toy
====

# Summary

This is an example toy local application that implements basic RAG queries for documents, based on
OpenAI ChatGPT API and embedding-based Vector Search.

Currently under construction. Please stay tuned!

# Quick Start

The project is setup by [poetry](https://python-poetry.org/). Use `poetry` to install the project:

```
poetry install
poetry shell
```

Add `OPENAI_API_KEY` to `.env` file:

```
OPENAI_API_KEY=sk-xxxx
```

After the above setup, run the `ragtoy` cli entry. For example, to add a new document:

```sh
ragtoy document add <path to doc>
```

To chat with all the documents:

```sh
# start interactive chat loop
 % ragtoy chat
question > What year was Alan Turing born?
Alan Turing was born on June 23, 1912.
========================================
Sources:
Node ID: 31b33cbf-2a48-4b2b-8f44-1f239dc22e45
Text: 6 Google LaMDA chatbot 7 Conferences  7.1 Turing Colloquium 7.2
...
```