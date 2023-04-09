from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskapp.llm import LLM
from flaskapp.vector import VectorIndices


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

llm = LLM()

vectorindices = VectorIndices()