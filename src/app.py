import os
import sys
import logging

from ui.app import GradioApp
from models.base import Base, engine

logging.basicConfig(encoding='utf-8', level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)


if not os.path.exists('/tmp/test.db'):
    Base.metadata.create_all(engine)


def main():
    GradioApp().launch(server_name='0.0.0.0')


if __name__ == '__main__':
    main()
