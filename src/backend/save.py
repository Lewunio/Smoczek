import json
from datetime import datetime, timedelta

from .pet import Pet


def save_game(pet: Pet, filename: str="src/backend/save.json"):
    """
    Zapisuje stan zwierzaka do pliku JSON.

    Przekształca dane obiektu Pet do formatu słownika i zapisuje
    je do wskazanego pliku w formacie JSON. Dodaje również datę zapisu.

    Args:
        pet (Pet): Obiekt reprezentujący zwierzaka do zapisania.
        filename (str): Ścieżka do pliku, do którego zapisane zostaną dane.

    Returns:
        None
    """
    try:
        data = {
            "name": pet.name,
            "species": pet.species,
            "birth": pet.birth.__str__(),
            "happy": pet.happy,
            "hunger": pet.hunger,
            "exp": pet.exp,
            "tired": pet.tired,
            "hunger_level": pet.hunger_level,
            "happy_level": pet.happy_level,
            "save_date": datetime.today().isoformat().__str__()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Błąd zapisu: {e}")

def load_game(filename: str="src/backend/save.json") -> Pet:
    """
    Wczytuje stan gry z pliku JSON i odtwarza obiekt Pet.

    Odczytuje dane zapisane w pliku i rekonstruuje obiekt klasy Pet,
    uzupełniając go również o aktualizację stanu na podstawie różnicy
    czasu między zapisem a obecnym momentem.

    Args:
        filename (str): Ścieżka do pliku z danymi w formacie JSON.

    Returns:
        Pet: Odtworzony obiekt zwierzaka.
    """

    with open(filename, "r") as f:
        data = json.load(f)
    print(f"Gra została wczytana z pliku '{filename}'.")
    pet = Pet(name=data["name"],
              species=data["species"],
              birth=data["birth"],
              happy=data["happy"],
              hunger=data["hunger"],
              exp=data["exp"],
              tired=data["tired"],
              hunger_level=data["hunger_level"],
              happy_level=data["happy_level"])
    time = datetime.fromisoformat(data["save_date"])
    load_time = datetime.now()
    pet.hunger = data["hunger"]
    pet.happy = data["happy"]
    while time < load_time:
        pet.update_stats()
        time = time + timedelta(minutes=1)

    return pet
    
