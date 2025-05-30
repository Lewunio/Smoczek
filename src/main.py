from datetime import datetime
from time import sleep

from backend import Pet
from frontend import gui


def main():
    pass
    # pet = Pet("Adas",0)
    pet2 = Pet(
        name="Milo",
        species=1,
        birth=datetime(2025, 5, 1),
        happy=85,
        hunger=30,
        tired=20,
        exp=120
    )
    gui.menu()
    # print(pet)
    # print(pet2)
    # while True:
    #     pet.update()
    #     # pet2.update()
    #     print(pet)
    #     sleep(5)
    #     # print(pet2)
    #     pet.feed(20)
if __name__ == "__main__":
    main()
