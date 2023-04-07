import sys
import logging
from argparse import ArgumentParser

from flask_restful import Api

from flaskapp.resources import (
    DocumentsApi, DocumentApi, ConversationsApi, ConversationApi,
    MessagesApi,
)
from flaskapp.config import app, db


api = Api(app)
api.add_resource(DocumentsApi, '/documents')
api.add_resource(DocumentApi, '/documents/<string:docid>')
api.add_resource(ConversationsApi, '/conversations')
api.add_resource(ConversationApi, '/conversations/<string:convid>')
api.add_resource(MessagesApi, '/conversations/<string:convid>/messages')


def initapp():
    with app.app_context():
        db.create_all()


def runapp():
    app.run()


if __name__ == '__main__':
    argparser = ArgumentParser(description='Run GptBot application')

    subparsers = argparser.add_subparsers(dest='command')
    initcmd = subparsers.add_parser('init')

    runcmd = subparsers.add_parser('run')

    args = argparser.parse_args()

    if args.command == 'init':
        initapp()
    elif args.command == 'run':
        runapp()
    else:
        argparser.print_help()
        logging.error('No command specified')
        sys.exit(1)
