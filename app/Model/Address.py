class Address:
    """
    Class representing an address
    """
    def __init__(self, city:str, street: str, country: str, number: int, zip_code: int):
        self._street = street
        self._number = number
        self._city = city
        self._country = country
        self._zip_code = zip_code
    
    def street(self) -> str:
        return self._street
    
    def number(self) -> int:
        return self._number
    
    def city(self) -> str:
        return self._city
    
    def country(self) -> str:
        return self._country
    
    def zip_code(self) -> int:
        return self._zip_code

    def __eq__(self, other):
        return self.street() == other.street() and self.number() == other.number() and self.city() == other.city() and self.country() == other.country() and self.zip_code() == other.zip_code()


    def __str__(self):
        return f"{self.street()} {self.number()}, {self.zip_code()} {self.city()}, {self.country()}"
    
    def __repr__(self):
        return f"{self.street()} {self.number()}, {self.zip_code()} {self.city()}, {self.country()}"