import sys
import logging
import argparse

from chattoy.client import Client


def get_doc(args):
    cli = Client(args.server)
    docs = []
    if not args.docids:
        docs = cli.get_documents()
    for docid in args.docids:
        docs.append(cli.get_document(docid))

    for doc in docs:
        print(doc)


def post_doc(args):
    cli = Client(args.server)

    name = args.name
    path = args.path
    doctype = args.type

    if doctype == 'text':
        with open(path, 'r') as f:
            doc = f.read()

            resp = cli.post_document(name, doctype, doc)
            print(resp)

    print(f'doc {name}, path {path}')


def main():
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description="A simple chat toy application cli")
    parser.add_argument('--server', action='store',
                        default='http://localhost:5000',
                        help='the remote API server address')
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Add document operations
    doc_parser = subparsers.add_parser('doc', help='manage documents')
    doc_parsers = doc_parser.add_subparsers(title='doc', dest="command")

    # post document get operations
    post_doc_cmd = doc_parsers.add_parser('post', help='post a new document')
    post_doc_cmd.add_argument(
        '--type', type=str, action='store', default='text', help='document type')
    post_doc_cmd.add_argument('name', type=str, help='document name')
    post_doc_cmd.add_argument('path', type=str, help='document path')
    post_doc_cmd.set_defaults(func=post_doc)

    # Add document get operations
    get_doc_cmd = doc_parsers.add_parser('get', help='get documents')
    get_doc_cmd.add_argument(
        'docids', type=str, nargs='*', help='document ids')
    get_doc_cmd.set_defaults(func=get_doc)

    # parse and execute
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
