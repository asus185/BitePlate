from typing import List
from patterns.command import KitchenQueue, PrepareOrderCommand, CancelOrderCommand, CompleteOrderCommand

class KitchenService:
    """Oshxona xizmati"""
    
    def __init__(self):
        self._queue = KitchenQueue()
    
    @property
    def queue(self) -> KitchenQueue:
        return self._queue
    
    def add_order_to_queue(self, order):
        """Buyurtmani oshxona navbatiga qo'shish"""
        command = PrepareOrderCommand(order)
        self._queue.add_command(command)
    
    def cancel_order(self, order):
        """Buyurtmani bekor qilish"""
        command = CancelOrderCommand(order)
        self._queue.add_command(command)
    
    def complete_order(self, order):
        """Buyurtmani tugatish"""
        command = CompleteOrderCommand(order)
        self._queue.add_command(command)
    
    def process_next(self):
        """Keyingi buyurtmani bajarish"""
        self._queue.execute_next()
    
    def process_all(self):
        """Barcha buyurtmalarni bajarish"""
        self._queue.execute_all()
    
    def undo_last(self):
        """Oxirgi amalni bekor qilish"""
        self._queue.undo_last()
    
    def get_queue_status(self) -> List[str]:
        """Navbat holati"""
        return self._queue.get_queue_status()
