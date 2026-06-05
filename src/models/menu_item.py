from abc import ABC, abstractmethod
from typing import List

class MenuItem(ABC):
    """Asosiy menyu elementi - barcha ovqatlar uchun abstract class"""
    
    def __init__(self, item_id: str, name: str, base_price: float, description: str = ""):
        self._item_id = item_id
        self._name = name
        self._base_price = base_price
        self._description = description
        self._allergens: List[str] = []
        self._available = True
    
    @property
    def item_id(self) -> str:
        return self._item_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def base_price(self) -> float:
        return self._base_price
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def allergens(self) -> List[str]:
        return self._allergens.copy()
    
    @property
    def available(self) -> bool:
        return self._available
    
    @available.setter
    def available(self, value: bool):
        self._available = value
    
    def add_allergen(self, allergen: str):
        """Allergen qo'shish"""
        if allergen not in self._allergens:
            self._allergens.append(allergen)
    
    @abstractmethod
    def get_price(self) -> float:
        """Narxni hisoblash - har bir subclass o'zicha implement qiladi"""
        pass
    
    def __str__(self) -> str:
        return f"{self.name} - ${self.get_price():.2f}"


class Starter(MenuItem):
    """Boshlang'ich taomlar"""
    
    def __init__(self, item_id: str, name: str, base_price: float, description: str = "", portion_size: str = "Regular"):
        super().__init__(item_id, name, base_price, description)
        self._portion_size = portion_size
    
    def get_price(self) -> float:
        return self._base_price
    
    def __str__(self) -> str:
        return f"[Starter] {super().__str__()}"


class MainCourse(MenuItem):
    """Asosiy taomlar"""
    
    def __init__(self, item_id: str, name: str, base_price: float, description: str = "", spiciness: int = 0):
        super().__init__(item_id, name, base_price, description)
        self._spiciness = spiciness
    
    def get_price(self) -> float:
        return self._base_price
    
    def __str__(self) -> str:
        return f"[Main] {super().__str__()}"


class Dessert(MenuItem):
    """Shirinliklar"""
    
    def __init__(self, item_id: str, name: str, base_price: float, description: str = "", is_seasonal: bool = False):
        super().__init__(item_id, name, base_price, description)
        self._is_seasonal = is_seasonal
    
    def get_price(self) -> float:
        return self._base_price
    
    def __str__(self) -> str:
        return f"[Dessert] {super().__str__()}"


class Beverage(MenuItem):
    """Ichimliklar"""
    
    def __init__(self, item_id: str, name: str, base_price: float, description: str = "", size: str = "Medium", is_alcoholic: bool = False):
        super().__init__(item_id, name, base_price, description)
        self._size = size
        self._is_alcoholic = is_alcoholic
    
    def get_price(self) -> float:
        size_multipliers = {"Small": 0.8, "Medium": 1.0, "Large": 1.3}
        return self._base_price * size_multipliers.get(self._size, 1.0)
    
    def __str__(self) -> str:
        return f"[Beverage] {super().__str__()}"
