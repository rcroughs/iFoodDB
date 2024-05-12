from enum import Enum

class PriceRange(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def int(self) -> int:
        return self.value
    
    def __str__(self):
        return self.name.lower()