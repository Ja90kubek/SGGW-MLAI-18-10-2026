
from logger import Logger
from file_writer import FileWriter
from safe_division import SafeDivision


def main():

    print(" ZADANIE 1: LOGGER ")

    with Logger():
        print("Wykonuję operację wewnątrz bloku with")

    print("\n ZADANIE 2: FILEWRITER ")

    with FileWriter("wynik.txt") as file:
        file.write("Pierwszy zapis do pliku.\n")
        file.write("Projekt SGGW - Context Managers.\n")

    print("Tekst został zapisany do pliku wynik.txt")


    print("\nZADANIE 3: OBSLUGA WYJATKOW ")

    try:
        with FileWriter("test_bledu.txt") as file:
            file.write("Test zapisu przed wystapieniem bledu.\n")
            raise ValueError("Przykladowy blad zapisu")

    except ValueError as error:
        print(f"Wyjatek przechwycony poza blokiem with: {error}")


    print("\nZADANIE 4: SAFEDIVISION")

    with SafeDivision() as division:
        result = division.divide(10, 2)
        print(f"10 / 2 = {result}")

    with SafeDivision() as division:
        result = division.divide(10, 0)
        print(f"10 / 0 = {result}")

    print("Program działa dalej po obsłużeniu wyjątku.")

if __name__ == "__main__":
    main()
