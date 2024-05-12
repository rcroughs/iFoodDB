from app.Model.Dish import Dish

class Menu:
    def __init__(self, dishes: list[Dish]):
        self._dishes = dishes

    def __str__(self):
        return ', '.join([str(dish) for dish in self._dishes])

    def __iter__(self):
        return iter(self._dishes)

    def __next__(self):
        return next(self._dishes)
    
    def __eq__(self, other):
        return self._dishes == other.dishes
    
    def dishes(self) -> list[Dish]:
        return self._dishes
    
    def __repr__(self):
        return ', '.join([str(dish) for dish in self._dishes])