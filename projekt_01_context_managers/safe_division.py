
class SafeDivision:

    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True

        return False
