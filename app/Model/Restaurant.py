from app.Model.Address import Address
from app.Model.PriceRange import PriceRange
from app.Model.Menu import Menu

class Restaurant:
    def __init__(self, name: str, address: Address, delivery: bool, evaluation: float, menu: Menu, opening: int, closing: int, price_range: PriceRange, type: str, id: int = None):
        self._name = name
        self._address = address
        self._delivery = delivery
        self._evaluation = evaluation
        self._menu = menu
        self._opening = opening
        self._closing = closing
        self._price_range = price_range
        self._type = type
        self._id = id

    def name(self) -> str:
        return self._name
    
    def address(self) -> Address:
        return self._address

    def delivery(self) -> bool:
        return self._delivery

    def evaluation(self) -> float:
        return self._evaluation
    
    def menu(self) -> Menu:
        return self._menu
    
    def opening(self) -> int:
        return self._opening
    
    def closing(self) -> int:
        return self._closing
    
    def price_range(self) -> PriceRange:
        return self._price_range
    
    def type(self) -> str:
        return self._type

    def id(self) -> int:
        return self._id

    def get_all_allergens(self) -> set:
        allergens = set()
        for dish in self._menu.dishes():
            allergens.update(dish.allergens())
        return allergens
    
    def __eq__(self, other):
        return self._name == other.name and self._address == other.address and self._delivery == other.delivery and self._evaluation == other.evaluation and self._menu == other.menu and self._opening == other.opening and self._closing == other.closing and self._price_range == other.price_range and self._type == other.type

    def __str__(self):
        return f"Name: {self._name}\nAddress: {self._address}\nDelivery: {self._delivery}\nEvaluation: {self._evaluation}\nMenu: {self._menu}\nOpening: {self._opening}\nClosing: {self._closing}\nPrice Range: {self._price_range}\nType: {self._type}"

    def __repr__(self):
        return self.__str__()