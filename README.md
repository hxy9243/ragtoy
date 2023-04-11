Chat Toy
====

# Summary

A toy application to ask questions about a document from the user, based on
OpenAI ChatGPT API.

Currently under construction. Please stay tuned!

# Demo

For a local demo run

1. Prepare for environment

   Install dependencies from `requirements.txt`.
   And go into `src/flaskapp` directory, creates `.env` environment file
   with your openAI token:

    ```
    OPENAI_API_KEY=sk-xxxx
    ```

2. Starts redis server

   ```
   docker run -d --restart=always -p 6379:6379 -p 8000:8000 redis-stack-server
   ```

   See:

   - <https://redis.io/docs/stack/>
   - <https://redis.io/docs/stack/get-started/install/docker/>

2. Start Flask app server

    ```
    flask run
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
