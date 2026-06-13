from enum import Enum
from typing import Optional
from datetime import datetime

class TableStatus(Enum):
    """Stol holati"""
    FREE = "Free"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"
    AWAITING_BILL = "Awaiting Bill"
    CLEARED = "Cleared"

class Table:
    """Stol boshqaruvi"""
    
    def __init__(self, table_number: int, capacity: int, location: str = "Main Hall"):
        self._table_number = table_number
        self._capacity = capacity
        self._location = location
        self._status = TableStatus.FREE
        self._current_order_id: Optional[str] = None
        self._reservation_id: Optional[str] = None
        self._occupied_at: Optional[datetime] = None
        self._cleared_at: Optional[datetime] = None
    
    @property
    def table_number(self) -> int:
        return self._table_number
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def location(self) -> str:
        return self._location
    
    @property
    def status(self) -> TableStatus:
        return self._status
    
    @property
    def current_order_id(self) -> Optional[str]:
        return self._current_order_id
    
    @property
    def reservation_id(self) -> Optional[str]:
        return self._reservation_id
    
    def occupy(self, order_id: str) -> bool:
        """Stolni egallash"""
        if self._status == TableStatus.FREE:
            self._status = TableStatus.OCCUPIED
            self._current_order_id = order_id
            self._occupied_at = datetime.now()
            return True
        return False
    
    def reserve(self, reservation_id: str) -> bool:
        """Stolni band qilish"""
        if self._status == TableStatus.FREE:
            self._status = TableStatus.RESERVED
            self._reservation_id = reservation_id
            return True
        return False
    
    def await_bill(self) -> bool:
        """Bill kutilmoqda"""
        if self._status == TableStatus.OCCUPIED:
            self._status = TableStatus.AWAITING_BILL
            return True
        return False
    
    def clear(self) -> bool:
        """Stolni tozalash"""
        if self._status in [TableStatus.AWAITING_BILL, TableStatus.OCCUPIED]:
            self._status = TableStatus.CLEARED
            self._current_order_id = None
            self._reservation_id = None
            self._cleared_at = datetime.now()
            return True
        return False
    
    def free_up(self) -> bool:
        """Stolni bo'shatish"""
        self._status = TableStatus.FREE
        self._current_order_id = None
        self._reservation_id = None
        self._occupied_at = None
        self._cleared_at = None
        return True
    
    def __str__(self) -> str:
        return f"Table {self._table_number} ({self._capacity}p) - {self._status.value}"
