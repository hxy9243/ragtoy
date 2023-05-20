import sys
import logging
from argparse import ArgumentParser

from flaskapp.app import initapp, runapp


def main():
    argparser = ArgumentParser(description='Run GptBot application')

    subparsers = argparser.add_subparsers(dest='command')
    subparsers.add_parser('init')
    subparsers.add_parser('run')

    args = argparser.parse_args()

    if args.command == 'init':
        initapp()
    elif args.command == 'run':
        runapp(debug=True)
    else:
        argparser.print_help()
        logging.error('No command specified')
        sys.exit(1)


if __name__ == '__main__':
    main()
