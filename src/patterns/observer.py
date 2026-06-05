from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Observer Pattern - Kuzatuvchi interface"""
    
    @abstractmethod
    def update(self, subject):
        pass

class Subject(ABC):
    """Kuzatiluvchi subject interface"""
    
    @abstractmethod
    def attach(self, observer: Observer):
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify(self):
        pass

class WaiterNotifier(Observer):
    """Waiter uchun bildirishnoma"""
    
    def __init__(self, waiter_id: str):
        self._waiter_id = waiter_id
        self._notifications: List[str] = []
    
    def update(self, subject):
        message = f"Waiter {self._waiter_id}: Order {subject.order_id} status changed to {subject.status}"
        self._notifications.append(message)
    
    def get_notifications(self) -> List[str]:
        return self._notifications.copy()

class ManagerDashboard(Observer):
    """Manager dashboard uchun bildirishnoma"""
    
    def __init__(self):
        self._alerts: List[str] = []
    
    def update(self, subject):
        message = f"ALERT: Order {subject.order_id} | Table {subject.table_number} | Status: {subject.status}"
        self._alerts.append(message)
    
    def get_alerts(self) -> List[str]:
        return self._alerts.copy()

class KitchenDisplay(Observer):
    """Oshxona displeyi"""
    
    def __init__(self):
        self._orders: List[dict] = []
    
    def update(self, subject):
        order_info = {
            "order_id": subject.order_id,
            "table_number": subject.table_number,
            "status": subject.status,
            "items": [str(item) for item in subject.items]
        }
        self._orders.append(order_info)
    
    def get_orders(self) -> List[dict]:
        return self._orders.copy()

class AllergyAlert(Observer):
    """Allergen ogohlantirishi"""
    
    def __init__(self):
        self._alerts: List[str] = []
    
    def update(self, subject):
        if hasattr(subject, 'allergens') and subject.allergens:
            message = f"ALLERGY ALERT: Order {subject.order_id} contains {subject.allergens}"
            self._alerts.append(message)
    
    def get_alerts(self) -> List[str]:
        return self._alerts.copy()

class OrderSubject(Subject):
    """Order - Kuzatiluvchi subject"""
    
    def __init__(self, order):
        self._order = order
        self._observers: List[Observer] = []
    
    @property
    def order_id(self):
        return self._order.order_id
    
    @property
    def table_number(self):
        return self._order.table_number
    
    @property
    def status(self):
        return self._order.status
    
    @property
    def items(self):
        return self._order.items
    
    @property
    def allergens(self):
        all_allergens = []
        for item in self._order.items:
            all_allergens.extend(item.menu_item.allergens)
        return list(set(all_allergens))
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    def set_status(self, new_status):
        """Status o'zgartirish va kuzatuvchilarni xabardor qilish"""
        self._order.status = new_status
        self.notify()
