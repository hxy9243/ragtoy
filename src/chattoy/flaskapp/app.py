

class App:

    def __init__(self):
        self.llm = None
        self.db = None
        self.vector = None


class Documents:
    def __init__(self) -> None:
        pass

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

    


class Messages:
    def __init__(self) -> None:
        pass

    def query(self, prompt: str) -> str:
        pass

    def get(self) -> List[str]:
        pass
