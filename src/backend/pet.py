from datetime import datetime


class Pet:

    def __init__(self, name:str, species:str, birth:datetime=datetime.today(), tired:float=100, happy:float=100, hunger:float=100, exp:float=0, hunger_level:float=100, happy_level:float=100):
        """
        Konstruktor klasy Pet

        Args:
            name(str): Imie zwierzaka
            species(str): Typ zwierzaka
            birth(datetime): Data urodzenia
            happy(float): Wskaznik szczescia
            hunger(float): Wskaznik glodu
            tired(float): Wskaznik zmeczenia
            exp(float): Ilosc doswiadczenia
            hunger_level(float): Jaki max głodu
            happy_level(float): Jaki max szczęścia z zabawy
        """
        self.name = name
        self.species = species
        self.birth = birth
        self.happy = happy
        self.hunger = hunger_level
        self.tired = tired
        self.exp = exp
        self.hunger_level = hunger_level
        self.happy_level = happy_level
        self.sleeping = False

    def sleep(self):
        """Zwierzak spi"""
        self.sleeping = not self.sleeping
        if self.tired < 95:
            if self.sleeping:
                self.tired = min(100.0, self.tired +2)
                self.exp += 1

    def eat(self):
        """Karmienie zwierzaka"""
        if self.hunger < self.hunger_level*0.95:
            self.hunger = min(self.hunger_level, self.hunger + 20)
            self.exp += 5

    def play(self):
        """
        Zabawa ze zwierzakiem.
        Zwieksza wskaznik szczescia i zmniejsza najedzenie i zwieksza sennosc.
        """
        if self.happy > self.happy_level*0.95:
            self.happy = min(self.happy_level, self.happy + 20)
            self.tired = max(0.0, self.tired - 10)
            self.hunger = max(0.0, self.hunger - 10)
            self.exp += 10
    def update_stats(self):
        """
        Aktualizuje status zwierzaka
        """
        self.hunger = max(0.0, self.hunger - 0.5)
        self.tired = max(0.0, self.tired - 0.5)
        if not self.sleeping:
            self.happy = max(0.0, self.happy - 0.5)

    def __str__(self):
        """
        ToString zwierzaka
        """
        return (f"Name: {self.name}\n"
                f"Species: {self.species}\n"
                f"Birth date: {self.birth}\n"
                f"Happiness: {self.happy}/100\n"
                f"Hunger: {self.hunger}/100\n"
                f"Tiredness: {self.tired}/100\n"
                f"Experience: {self.exp}")
