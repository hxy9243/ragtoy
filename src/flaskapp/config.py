import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskapp.nlp import LLM
from flaskapp.vector import VectorIndices


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
llm = LLM(openai_api_key=api_key)

vectorindices = VectorIndices('localhost', 6379)
