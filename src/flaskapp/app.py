from flask_restful import Api
from flask import Blueprint
from flask_cors import CORS

from flaskapp.resources import (
    DocumentsApi, DocumentApi, DocumentConversationsApi,
    ConversationsApi, ConversationApi,
    MessagesApi,
)
from flaskapp.config import app, db

apibp = Blueprint('api', __name__)
api = Api(apibp)
api.add_resource(DocumentsApi, '/documents')
api.add_resource(DocumentApi, '/documents/<string:docid>')
api.add_resource(DocumentConversationsApi,
                 '/documents/<string:docid>/conversations')
api.add_resource(ConversationsApi, '/conversations')
api.add_resource(ConversationApi, '/conversations/<string:convid>')
api.add_resource(MessagesApi, '/conversations/<string:convid>/messages')

app.register_blueprint(apibp, url_prefix='/api')

CORS(app)


def initapp():
    with app.app_context():
        db.create_all()


def runapp(*args, **kwargs):
    app.run(*args, **kwargs)
