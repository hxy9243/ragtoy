Chat Toy
====

# Summary

A toy application that implements basic RAG queries for documents, based on
OpenAI ChatGPT API and Redit Vector Search.

Currently under construction. Please stay tuned!

# Demo

For a local demo run

1. Prepare for environment

   - Install dependencies from `pyproject` with `poetry install`. This will install:

      - `chattoy_server`: the server application that manages running the backend service.
      - `chattoy`: the example client.

   - Creates `.env` environment file for your openAI token:

   ```
   OPENAI_API_KEY=sk-xxxx
   ```

2. Starts redis server for vector indexing

   Start redis stack server manually, or use docker:

   ```
   docker run -d --restart=always -p 6379:6379 -p 8000:8000 redis/redis-stack-server
   ```

   See:

   - <https://redis.io/docs/stack/>
   - <https://redis.io/docs/stack/get-started/install/docker/>

2. Init database and start Flask app server

   Init database

   ```
   chattoy_server init
   chattoy_server run
   ```

3. Queries API interface

   See definition in [app.py](src/flaskapp/app.py).
   (Documentation to come soon...)

   e.g.:

   ```
   curl -XPOST -H 'content-type=application/json' -d @data.json localhost:5000/documents
   ```

   data.json:

   ```
   {"document": "example text here.", "type": "text"}
   ```
