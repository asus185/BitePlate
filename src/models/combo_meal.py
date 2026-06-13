from typing import List
from models.menu_item import MenuItem

class ComboMeal:
    """Kombo yoki Set Meal - bir nechta MenuItem'larni birlashtiradi"""
    
    def __init__(self, combo_id: str, name: str, discount_percent: float = 10.0):
        self._combo_id = combo_id
        self._name = name
        self._items: List[MenuItem] = []
        self._discount_percent = discount_percent
    
    @property
    def combo_id(self) -> str:
        return self._combo_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def items(self) -> List[MenuItem]:
        return self._items.copy()
    
    def add_item(self, item: MenuItem):
        """Kombo'ga element qo'shish"""
        self._items.append(item)
    
    def remove_item(self, item_id: str) -> bool:
        """Kombo'dan element olib tashlash"""
        for item in self._items:
            if item.item_id == item_id:
                self._items.remove(item)
                return True
        return False
    
    def get_total_price(self) -> float:
        """Chegirma bilan narxni hisoblash"""
        original_total = sum(item.get_price() for item in self._items)
        discount_amount = original_total * (self._discount_percent / 100)
        return original_total - discount_amount
    
    def __str__(self) -> str:
        return f"[Combo] {self.name} - ${self.get_total_price():.2f} ({len(self._items)} items)"
