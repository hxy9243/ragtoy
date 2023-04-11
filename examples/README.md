ChatGPT Example
========

This is a toy Python project to learn and explore the capabilities of openAI ChatGPT API.

# Project Setup

Project requires your openAI key in `.env` file:

```
OPENAI_API_KEY=sk-example-key
```

# Examples

## Wikipedia Q & A machine. [examples/wiki_qa.py](examples/wiki_qa.py)

Usage:

```
cd examples
python3 wiki_qa.py

## Enter your question based in input.
```

Update `WIKI_PAGE` constant to get more info on different pages and topics.

Example output:

```
Question: What was Turing test and how did Alan describe it?

Calling openAI completion API...
Prompt:  Answer the question based on the context, and if it cannot be answered based on the context, say "I don't know"
Context:
Figure adapted from Saygin, 2000.[7] Saul Traiger argues that there are at least three primary versions of the Turing test, two of which are offered in "Computing Machinery and Intelligence" and one that he describes as the "Standard Interpretation".[55] While there is some debate regarding whether the "Standard Interpretation"

...

====================


openAI answer: Turing test was a test of indistinguishability in performance capacity, where an interrogator would ask questions of a machine and a human in order to determine which was which. Alan Turing described it as a three-person game involving an interrogator asking questions of a man and a woman in another room in order to determine the correct sex of the two players.


====================
```

Update `WIKI_PAGE` constant to get more info on different pages and topics.
