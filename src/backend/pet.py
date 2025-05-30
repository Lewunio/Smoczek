from datetime import datetime


class Pet:
    def __init__(self, name:str, species:int, birth:datetime=datetime.today(), tired:float=100, happy:float=100, hunger:float=100, exp:float=0):
        """
        Klasa Zwierzaka

        Args:
            name(str): Imie zwierzaka
            species(int): Typ zwierzaka
            birth(datetime): Data urodzenia
            happy(float): Wskaznik szczescia
            hunger(float): Wskaznik glodu
            tired(float): Wskaznik zmeczenia
            exp(float): Ilosc doswiadczenia
        """
        self.name = name
        self.species = species
        self.birth = birth
        self.happy = happy
        self.hunger = hunger
        self.tired = tired
        self.exp = exp

    def sleep(self):
        """Zwierzak spi"""
        self.tired = min(100, self.tired +20)
        self.exp += 5

    def eat(self):
        """Karmienie zwierzaka"""
        self.hunger = min(100, self.hunger + 20)
        self.exp += 5

    def play(self):
        """
        Zabawa ze zwierzakiem.
        Zwieksza wskaznik szczescia i zmniejsza najedzenie i zwieksza sennosc.
        """
        self.happy = min(100, self.happy + 20)
        self.tired = max(0, self.tired - 10)
        self.hunger = max(0, self.hunger - 10)
        self.exp += 10
    def update_stats(self):
        self.hunger = max(0, self.hunger - 0.5)
        self.tired = max(0, self.tired - 0.5)
        self.happy = max(0, self.happy - 0.5)
    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Species: {self.species}\n"
                f"Birth date: {self.birth}\n"
                f"Happiness: {self.happy}/100\n"
                f"Hunger: {self.hunger}/100\n"
                f"Tiredness: {self.tired}/100\n"
                f"Experience: {self.exp}")