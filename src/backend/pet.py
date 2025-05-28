from datetime import datetime


class Pet:
    def __init__(self, name:str, species:int, birth:datetime=datetime.today(), happy:float=100, hunger:float=100, difficulty:int=0):
        """
        Klasa Zwierzaka

        Args:
            name(str): Imie zwierzaka
            species(int): Typ zwierzaka
            birth(datetime): Data urodzenia
            happy(float): Wskaznik szczescia
            hunger(float): Wskaznik glodu
            difficulty(int): Trudnosc gry
        """
        self.name = name
        self.species = species
        self.birth = birth
        self.happy = happy
        self.hunger = hunger
        self.difficult = difficulty

    def feed(self, food:float):
        """
        Karmienie zwierzaka

        Args:
            food(float): Wartosc odzywca

        Returns:
            None
        """
        self.hunger += food

    def play(self, fun:float):
        """
        Zabawa ze zwierzakiem.
        Zwieksza wskaznik szczescia i zmniejsza najedzenie.

        Args:
            fun(float): Jak bardzo maleje znudzenie

        Returns:

        """
        self.happy += fun
        self.hunger -= fun/10