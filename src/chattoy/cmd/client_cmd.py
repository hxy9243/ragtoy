import sys
import logging
import argparse

from chattoy.client import Client

from chattoy.client.models import ConversationRequest


def post_doc(args):
    cli = Client(args.server)

    name = args.name
    path = args.path
    doctype = args.type

    if doctype == "text":
        with open(path, "r") as f:
            doc = f.read()
            print(f"doc {name}, path {path}")
            resp = cli.post_document(name, doctype, doc)
            print(resp)
            return
    else:
        print(f'Unknown document type "{doctype}"', file=sys.stderr)
        return


def get_doc(args):
    cli = Client(args.server)
    docs = []
    if not args.docids:
        docs = cli.get_documents()
    for docid in args.docids:
        docs.append(cli.get_document(docid))

    for doc in docs:
        print(doc)


def del_doc(args):
    cli = Client(args.server)
    if not args.docids:
        print("no document id specified")

    for docid in args.docids:
        doc = cli.delete_document(docid)
        print(f"Deleted document: {doc}")


def add_conv(args):
    cli = Client(args.server)
    r = cli.add_conversation(
        ConversationRequest(
            user=args.user,
            docid=args.docid,
        )
    )
    print(f"Added new conversation {r.convid}")


def get_conv(args):
    cli = Client(args.server)

    if not args.convids:
        convs = cli.get_conversations()
        for conv in convs:
            print(conv)
    else:
        for convid in args.convids:
            conv = cli.get_conversation(convid)
            print(conv)


def del_conv(args):
    cli = Client(args.server)

    if not args.convids:
        print("Converstaion id not defined", file=sys.stderr)
        return

    for convid in args.convids:
        cli.delete_conversation(convid)


def main():
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="A simple chat toy application cli")
    parser.add_argument(
        "--server",
        action="store",
        default="http://localhost:5000",
        help="the remote API server address",
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Add document operations
    doc_parser = subparsers.add_parser("doc", help="manage documents")
    doc_parsers = doc_parser.add_subparsers(title="doc", dest="command")

    # post document get operations
    post_doc_cmd = doc_parsers.add_parser("add", help="post a new document")
    post_doc_cmd.add_argument(
        "--type", type=str, action="store", default="text", help="document type"
    )
    post_doc_cmd.add_argument("name", type=str, help="document name")
    post_doc_cmd.add_argument("path", type=str, help="document path")
    post_doc_cmd.set_defaults(func=post_doc)

    # get document get operations
    get_doc_cmd = doc_parsers.add_parser("list", help="get documents")
    get_doc_cmd.add_argument("docids", type=str, nargs="*", help="document ids")
    get_doc_cmd.set_defaults(func=get_doc)

    # del document get operations
    get_doc_cmd = doc_parsers.add_parser("del", help="delete documents")
    get_doc_cmd.add_argument("docids", type=str, nargs="*", help="document ids")
    get_doc_cmd.set_defaults(func=del_doc)

    # add converstaions
    conv_parser = subparsers.add_parser("conv", help="manage conversations")
    conv_parsers = conv_parser.add_subparsers(title="conv", dest="command")

    post_conv_cmd = conv_parsers.add_parser("add", help="add a new conversation")
    post_conv_cmd.add_argument(
        "--user",
        type=str,
        action="store",
        default="default-user",
        help="sepcifcy user",
    )
    post_conv_cmd.add_argument(
        "--docid", type=str, action="store", default="", help="document id"
    )
    post_conv_cmd.set_defaults(func=add_conv)

    get_conv_cmd = conv_parsers.add_parser("list", help="get conversations")
    get_conv_cmd.add_argument("convids", type=str, nargs="*", help="conversation ids")
    get_conv_cmd.set_defaults(func=get_conv)

    del_conv_cmd = conv_parsers.add_parser("del", help="delete conversations")
    del_conv_cmd.add_argument("convids", type=str, nargs="*", help="conversation ids")
    del_conv_cmd.set_defaults(func=del_conv)

    # parse and execute
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
