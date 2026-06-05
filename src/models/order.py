from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    """Buyurtma holatlari"""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"

class OrderItem:
    """Buyurtma elementi"""
    
    def __init__(self, menu_item, quantity: int = 1, customizations: Optional[dict] = None):
        self._menu_item = menu_item
        self._quantity = quantity
        self._customizations = customizations or {}
    
    @property
    def menu_item(self):
        return self._menu_item
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        self._quantity = value
    
    @property
    def customizations(self) -> dict:
        return self._customizations.copy()
    
    def get_total_price(self) -> float:
        return self._menu_item.get_price() * self._quantity
    
    def __str__(self) -> str:
        return f"{self._menu_item.name} x{self._quantity} - ${self.get_total_price():.2f}"

class Order:
    """Buyurtma"""
    
    def __init__(self, order_id: str, table_number: int, waiter_id: str):
        self._order_id = order_id
        self._table_number = table_number
        self._waiter_id = waiter_id
        self._items: List[OrderItem] = []
        self._status = OrderStatus.PENDING
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._notes = ""
    
    @property
    def order_id(self) -> str:
        return self._order_id
    
    @property
    def table_number(self) -> int:
        return self._table_number
    
    @property
    def waiter_id(self) -> str:
        return self._waiter_id
    
    @property
    def items(self) -> List[OrderItem]:
        return self._items.copy()
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @status.setter
    def status(self, value: OrderStatus):
        self._status = value
        self._updated_at = datetime.now()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, value: str):
        self._notes = value
    
    def add_item(self, menu_item, quantity: int = 1, customizations: Optional[dict] = None):
        """Buyurtmaga element qo'shish"""
        order_item = OrderItem(menu_item, quantity, customizations)
        self._items.append(order_item)
        self._updated_at = datetime.now()
    
    def remove_item(self, item_index: int) -> bool:
        """Buyurtmadan element olib tashlash"""
        if 0 <= item_index < len(self._items):
            self._items.pop(item_index)
            self._updated_at = datetime.now()
            return True
        return False
    
    def get_total(self) -> float:
        """Buyurtma umumiy narxi"""
        return sum(item.get_total_price() for item in self._items)
    
    def can_modify(self) -> bool:
        """Buyurtmani o'zgartirish mumkinmi?"""
        return self._status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def __str__(self) -> str:
        return f"Order #{self._order_id} | Table {self._table_number} | {self._status.value} | ${self.get_total():.2f}"
