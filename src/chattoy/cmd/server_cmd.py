import sys
import logging
from argparse import ArgumentParser

from chattoy.flaskapp.app import initapp, runapp


def main():
    argparser = ArgumentParser(description='Run GptBot application')

    subparsers = argparser.add_subparsers(dest='command')
    subparsers.add_parser('init')
    run_parser = subparsers.add_parser('run')

    run_parser.add_argument('--host', action='store',
                            default='127.0.0.1', dest='host',
                            help='The host IP for server to bind to')
    run_parser.add_argument('-p,--port', action='store',
                            default=5000, dest='port',
                            help='The port for server to listen on')
    run_parser.add_argument('-d,--debug', action='store_true',
                            dest='debug',
                            help='Turns on debug')

    args = argparser.parse_args()

    if args.command == 'init':
        initapp()
    elif args.command == 'run':
        runapp(
            host=args.host,
            port=args.port,
            debug=args.debug,
        )
    else:
        argparser.print_help()
        logging.error('No command specified')
        sys.exit(1)


if __name__ == '__main__':
    main()
