class Dish:
    def __init__(self, allergens: list[str], name: str, price: float):
        self._allergens = allergens
        self._name = name
        self._price = price

    def allergens(self) -> list[str]:
        return self._allergens
    
    def name(self) -> str:
        return self._name
    
    def price(self) -> float:
        return self._price
    
    def __eq__(self, other):
        return self._allergens == other.allergens and self._name == other.name and self._price == other.price

    def __str__(self):
        return f"Name: {self._name}\nPrice: {self._price}\nAllergens: {self._allergens}"
    
    def __repr__(self):
        return f"Name: {self._name}\nPrice: {self._price}\nAllergens: {self._allergens}"