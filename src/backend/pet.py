import threading
from datetime import datetime
from time import sleep


class Pet:
    """
    Klasa reprezentująca zwierzaka.

    Args:
        name (str): Imię zwierzaka.
        species (str): Gatunek zwierzaka.
        birth (datetime): Data urodzenia.
        happy (float): Wskaźnik szczęścia.
        hunger (float): Wskaźnik głodu.
        tired (float): Wskaźnik zmęczenia.
        exp (float): Poziom doświadczenia.
        hunger_level (float): Maksymalny poziom głodu.
        happy_level (float): Maksymalny poziom szczęścia.
        sleeping (bool): Czy zwierzak śpi.
    """
    def __init__(self, name:str, species:str, birth:datetime=datetime.today(), tired:float=100, exp:float=0, hunger_level:float=100, happy_level:float=100):
        """
        Inicjalizuje nowego zwierzaka.

        Args:
            name (str): Imię zwierzaka.
            species (str): Gatunek zwierzaka.
            birth (datetime, optional): Data urodzenia. Domyślnie: dzisiaj.
            tired (float, optional): Poziom zmęczenia. Domyślnie 100.
            exp (float, optional): Poziom doświadczenia. Domyślnie 0.
            hunger_level (float, optional): Maksymalny głód. Domyślnie 100.
            happy_level (float, optional): Maksymalne szczęście. Domyślnie 100.
        """
        self.name = name
        self.species = species
        self.birth = birth
        self.happy = happy_level
        self.hunger = hunger_level
        self.tired = tired
        self.exp = exp
        self.hunger_level = hunger_level
        self.happy_level = happy_level
        self.sleeping = False

    def sleep(self):
        """Wprowadza zwierzaka w stan snu lub go budzi."""
        self.sleeping = not self.sleeping
        th = threading.Thread(target=self.sleep_thread).start()


    def sleep_thread(self):
        """Wątek snu — regeneruje zmęczenie, gdy zwierzak śpi."""
        while self.sleeping:
            self.tired = min(100.0, self.tired +2)
            if self.tired != 100:
                self.exp += 1
            sleep(2)
    def eat(self):
        """Karmi zwierzaka, zwiększając poziom głodu i doświadczenie."""
        if self.can_eat:
            self.hunger = min(self.hunger_level, self.hunger + 5)
            self.exp += 5
    @property
    def can_eat(self) -> bool:
        """
        Sprawdza, czy zwierzak może jeść.

        Returns:
            bool: True, jeśli głodny i nie śpi.
        """
        return self.hunger < self.hunger_level*0.95 and not self.sleeping

    def play(self):
        """
        Bawi się ze zwierzakiem — zwiększa szczęście i zmniejsza głód.
        """
        if self.sleeping:
            return
        self.happy = min(self.happy_level, self.happy + 5)
        self.tired = max(0.0, self.tired - 5)
        self.hunger = max(0.0, self.hunger - 5)
        self.exp += 10
    def update_stats(self):
        """
        Aktualizuje statystyki zwierzaka, zmniejszając parametry życiowe.
        """
        self.happy = max(0.0, self.happy - 0.5)
        self.hunger = max(0.0, self.hunger - 0.5)
        if not self.sleeping:
            self.tired = max(0.0, self.tired - 0.5)

    def __str__(self):
        """
        Zwraca tekstową reprezentację zwierzaka.

        Returns:
            str: Opis zwierzaka.
        """
        return (f"Name: {self.name}\n"
                f"Species: {self.species}\n"
                f"Birth date: {self.birth}\n"
                f"Happiness: {self.happy}/100\n"
                f"Hunger: {self.hunger}/100\n"
                f"Tiredness: {self.tired}/100\n"
                f"Experience: {self.exp}")
