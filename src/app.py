import sys
import logging

from ui.app import GradioApp


logging.basicConfig(encoding='utf-8', level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)


def main():
    GradioApp().launch(server_name='0.0.0.0')


if __name__ == '__main__':
    main()
