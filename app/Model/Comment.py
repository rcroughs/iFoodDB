from app.Model.Recommendation import Recommendation

class Comment: 
    def __init__(self, user: str, comment: str, datecomm: str, restaurant: str, note: int, date: str, menu: list[str], price: float, begin_hour: int, end_hour: int, recommendation: Recommendation, noteservice: int = None, notedelivery: int = None):
        self._comment = comment
        self._date = date
        self._restaurant = restaurant
        self._note = note
        self._noteservice = noteservice
        self._datecomm = datecomm
        self._menu = menu
        self._price = price
        self._begin_hour = begin_hour
        self._end_hour = end_hour
        self._notedelivery = notedelivery
        self._recommendation = recommendation
        self._user = user

    def __str__(self):
        return f"{self._comment} - {self._date} - {self._restaurant} - {self._note} - {self._noteservice} - {self._datecomm} - {self._menu} - {self._price} - {self._begin_hour} - {self._end_hour} - {self._notedelivery}"
    
    def __repr__(self):
        return self.__str__()
    
    def user(self):
        return self._user

    def name(self):
        return self._user.split(" ")[1]

    def first_name(self):
        return self._user.split(" ")[0]

    def comment(self):
        return self._comment
    
    def date(self):
        return self._date
    
    def restaurant(self):
        return self._restaurant
    
    def note(self):
        return self._note
    
    def noteservice(self):
        return self._noteservice
    
    def datecomm(self):
        return self._datecomm
    
    def menu(self):
        return self._menu
    
    def price(self):
        return self._price
    
    def begin_hour(self):
        return self._begin_hour
    
    def end_hour(self):
        return self._end_hour
    
    def notedelivery(self):
        return self._notedelivery

    def recommendation(self):
        return self._recommendation
