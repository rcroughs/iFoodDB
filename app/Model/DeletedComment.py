from app.Model.Comment import Comment
from app.Model.Recommendation import Recommendation

class DeletedComment(Comment):
    def __init__(self, user: str, comment: str, datecomm: str, restaurant: str, note: int, date: str, menu: list[str], price: float, begin_hour: int, end_hour: int, recommendation: Recommendation, noteservice: int = None, notedelivery: int = None, mod_comment: str = None, mod_id: str = None):
        super().__init__(user, comment, datecomm, restaurant, note, date, menu, price, begin_hour, end_hour, recommendation, noteservice, notedelivery)
        self._mod_comment = mod_comment
        self._mod_id = mod_id

    def __str__(self):
        return f"{super().__str__()} - {self._mod_comment} - {self._mod_id}"
    
    def __repr__(self):
        return self.__str__()
    
    def mod_comment(self):
        return self._mod_comment
    
    def mod_id(self):
        return self._mod_id