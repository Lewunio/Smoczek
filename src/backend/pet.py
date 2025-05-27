from datetime import date


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.birth = date.today()
