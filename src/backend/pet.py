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

    def update(self):
        self.happy -= 0.5
        self.hunger -= 0.5
        self.tired -= 0.5

    def feed(self, food:float):
        """
        Karmienie zwierzaka

        Args:
            food(float): Wartosc odzywca

        Returns:
            None
        """
        self.hunger += food
        if self.hunger < 0:
            self.hunger = 0
        elif self.hunger > 100:
            self.hunger = 100

    def play(self, fun:float):
        """
        Zabawa ze zwierzakiem.
        Zwieksza wskaznik szczescia i zmniejsza najedzenie i zwieksza sennosc.

        Args:
            fun(float): Jak bardzo maleje znudzenie

        Returns:

        """
        self.happy += fun
        self.feed(-fun/10)
        if self.happy < 0:
            self.happy = 0
        elif self.happy > 100:
            self.happy = 100
    def sleep(self):
        """
        Zwierzak spi


        """
        self.tired+=1
        if self.tired > 100:
            self.tired = 100
        elif self.tired < 0:
            self.tired = 0
    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Species: {self.species}\n"
                f"Birth date: {self.birth}\n"
                f"Happiness: {self.happy}/100\n"
                f"Hunger: {self.hunger}/100\n"
                f"Tiredness: {self.tired}/100\n"
                f"Experience: {self.exp}")