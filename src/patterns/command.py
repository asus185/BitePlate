from abc import ABC, abstractmethod
from typing import List, Optional
from models.order import OrderStatus

class Command(ABC):
    """Command Pattern - Asosiy interface"""
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class PrepareOrderCommand(Command):
    """Buyurtmani tayyorlash"""
    
    def __init__(self, order):
        self._order = order
        self._previous_status = None
    
    def execute(self):
        self._previous_status = self._order.status
        self._order.status = OrderStatus.PREPARING
    
    def undo(self):
        if self._previous_status:
            self._order.status = self._previous_status
    
    def __str__(self) -> str:
        return f"Prepare Order: {self._order.order_id}"

class CancelOrderCommand(Command):
    """Buyurtmani bekor qilish"""
    
    def __init__(self, order):
        self._order = order
        self._previous_status = None
    
    def execute(self):
        self._previous_status = self._order.status
        self._order.status = OrderStatus.CANCELLED
    
    def undo(self):
        if self._previous_status:
            self._order.status = self._previous_status
    
    def __str__(self) -> str:
        return f"Cancel Order: {self._order.order_id}"

class CompleteOrderCommand(Command):
    """Buyurtmani tugatish"""
    
    def __init__(self, order):
        self._order = order
        self._previous_status = None
    
    def execute(self):
        self._previous_status = self._order.status
        self._order.status = OrderStatus.READY
    
    def undo(self):
        if self._previous_status:
            self._order.status = self._previous_status
    
    def __str__(self) -> str:
        return f"Complete Order: {self._order.order_id}"

class KitchenQueue:
    """Invoker - Oshxona navbati"""
    
    def __init__(self):
        self._queue: List[Command] = []
        self._history: List[Command] = []
    
    @property
    def queue(self) -> List[Command]:
        return self._queue.copy()
    
    @property
    def history(self) -> List[Command]:
        return self._history.copy()
    
    def add_command(self, command: Command):
        """Command qo'shish"""
        self._queue.append(command)
    
    def execute_next(self):
        """Keyingi command'ni bajarish va history'ga qo'shish"""
        if self._queue:
            command = self._queue.pop(0)
            command.execute()
            self._history.append(command)
    
    def execute_all(self):
        """Barcha command'larni bajarish"""
        while self._queue:
            self.execute_next()
    
    def undo_last(self):
        """Oxirgi command'ni bekor qilish"""
        if self._history:
            command = self._history.pop()
            command.undo()
    
    def get_queue_status(self) -> List[str]:
        """Navbat holati"""
        return [str(cmd) for cmd in self._queue]
    
    def clear_queue(self):
        """Navbatni tozalash"""
        self._queue.clear()
        self._history.clear()
