
class FileWriter:

    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                print(f"Błąd podczas zapisu: {exc_value}")
        finally:
            if self.file is not None:
                self.file.close()

        return False
