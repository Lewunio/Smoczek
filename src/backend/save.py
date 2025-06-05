import json
from datetime import datetime

from .pet import Pet


def save_game(pet: Pet, filename: str):
    """
        Zapisuje stan zwierzaka do pliku JSON.
        Przeksztalca dane zwierzaka na dict i zapisuje date.
        Args:
            pet (Pet): Dane zwierzaka do zapisu.
            filename (str): Nazwa pliku do zapisu.
        Returns:
            None
    """
    try:
        data = {
            "name": pet.name,
            "species": pet.species,
            "birth": pet.birth,
            "happy": pet.happy,
            "hunger": pet.hunger,
            "exp": pet.exp,
            "tired": pet.tired,
            "save_date": datetime.today().isoformat()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Stan został zapisany do pliku '{filename}'.")
    except Exception as e:
        print(f"Błąd zapisu: {e}")

def load_game(filename: str) -> Pet:
    """
        Wczytuje stan gry z pliku JSON.

        Args:
            filename (str): Nazwa pliku do wczytania.

        Returns:
            Pet: Nowy zwierzak z wczytanym stanem.
    """

    with open(filename, "r") as f:
        data = json.load(f)
    print(f"Gra została wczytana z pliku '{filename}'.")
    return data
    
