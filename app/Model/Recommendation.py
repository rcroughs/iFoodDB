from enum import Enum

class Recommendation(Enum):
    RECOMMENDED = 3
    NOT_RECOMMENDED = 2
    TO_BE_AVOIDED = 1

    def __str__(self):
        return self.name.lower().replace("_", " ")
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name
    
    def int(self):
        return self.value
