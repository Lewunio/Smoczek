import json

def save(data: dict, filename: str):
    """
        Zapisuje stan gry do pliku JSON.

        Args:
            data (dict): Dane gry do zapisu.
            filename (str): Nazwa pliku do zapisu.
        Returns:
            None
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Gra została zapisana do pliku '{filename}'.")
    except Exception as e:
        print(f"Błąd zapisu gry: {e}")

def load(filename: str) -> dict:
    """
        Wczytuje stan gry z pliku JSON.

        Args:
            filename (str): Nazwa pliku do wczytania.

        Returns:
            dict: Dane gry wczytane z pliku.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"Gra została wczytana z pliku '{filename}'.")
        return data
    except FileNotFoundError:
        print(f"Plik '{filename}' nie istnieje. Zwracam nowy stan gry.")
        return {}
    except Exception as e:
        print(f"Błąd wczytywania gry: {e}")
        return {}
