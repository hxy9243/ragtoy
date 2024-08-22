from typing import List

class Command:
    def __init__(self) -> None:
        doc = Documents()

    def ask(self, prompt: str):
        pass


class Documents:
    def __init__(self, cfg) -> None:
        cfg = cfg

    def add(self, path: str):
        pass

    def ls(self) -> List[str]:
        pass

    def rm(self, id: str):
        pass

    def search(self, prompt: str) -> List[str]:
        pass

    def related(self, docid: str, limit=5) -> List[str]:
        pass


def main():

    pass