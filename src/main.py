from datetime import datetime

from backend import Pet


def main():
    pet = Pet("Adas",0)
    pet2 = Pet(
        name="Milo",
        species=1,
        birth=datetime(2025, 5, 1),
        happy=85,
        hunger=30,
        tired=20,
        exp=120
    )
    print(pet)
    print(pet2)
if __name__ == "__main__":
    main()
