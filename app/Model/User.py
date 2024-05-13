from app.Model.Address import Address
from app.Model.Restaurant import Restaurant

class User:
    def __init__(self, name: str, first_name: str, address: Address, is_owner: bool, restaurants: list[Restaurant]= []):
        self._name = name
        self._first_name = first_name
        self._is_owner = is_owner
        self._address = address
        self._restaurants = restaurants
        self._is_mod = False

    def __str__(self):
        return f"{self._name} {self._first_name} - {self._address}"
    
    def __repr__(self):
        return self.__str__()
    
    def restaurants(self):
        return self._restaurants
    
    def add_restaurant(self, restaurant: Restaurant):
        self._restaurants.append(restaurant)

    def name(self):
        return self._name
    
    def first_name(self):
        return self._first_name
    
    def address(self):
        return self._address
    
    def is_owner(self):
        return self._is_owner

    def set_mod(self):
        self._is_mod = True
    
    def is_mod(self):
        return self._is_mod