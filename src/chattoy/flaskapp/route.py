from flask_restx import Api

from .resources import (
    DocumentsApi, DocumentApi, DocumentConversationsApi,
    ConversationsApi, ConversationApi,
    MessagesApi,
)


def create_api_route(app):
    api = Api(app)
    api.add_resource(DocumentsApi, '/documents')
    api.add_resource(DocumentApi, '/documents/<string:docid>')
    api.add_resource(DocumentConversationsApi,
                     '/documents/<string:docid>/conversations')
    api.add_resource(ConversationsApi, '/conversations')
    api.add_resource(ConversationApi, '/conversations/<string:convid>')
    api.add_resource(MessagesApi, '/conversations/<string:convid>/messages')

    return app
