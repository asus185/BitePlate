from typing import List, Optional, Dict
from models.order import Order, OrderStatus
from models.menu_item import MenuItem
from patterns.observer import OrderSubject, WaiterNotifier, ManagerDashboard, KitchenDisplay, AllergyAlert
from patterns.singleton import OrderHistoryLog

class OrderService:
    """Buyurtma xizmati"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._order_subjects: Dict[str, OrderSubject] = {}
        self._next_order_id = 1
        self._history_log = OrderHistoryLog()
    
    def create_order(self, table_number: int, waiter_id: str) -> Order:
        """Yangi buyurtma yaratish + observerlarni biriktirish"""
        order_id = f"ORD-{self._next_order_id:04d}"
        self._next_order_id += 1

        order = Order(order_id, table_number, waiter_id)
        self._orders[order_id] = order

        subject = OrderSubject(order)
        self._order_subjects[order_id] = subject

        # Default observerlarni avtomatik biriktirish
        subject.attach(WaiterNotifier(waiter_id))
        subject.attach(ManagerDashboard())
        subject.attach(KitchenDisplay())
        subject.attach(AllergyAlert())

        return order
    
    def add_item_to_order(self, order_id: str, menu_item: MenuItem, quantity: int = 1, customizations: Optional[dict] = None) -> bool:
        """Buyurtmaga element qo'shish"""
        order = self._orders.get(order_id)
        if order and order.can_modify():
            order.add_item(menu_item, quantity, customizations)
            self._notify_observers(order_id)
            return True
        return False
    
    def remove_item_from_order(self, order_id: str, item_index: int) -> bool:
        """Buyurtmadan element olib tashlash"""
        order = self._orders.get(order_id)
        if order and order.can_modify():
            return order.remove_item(item_index)
        return False
    
    def confirm_order(self, order_id: str) -> bool:
        """Buyurtmani tasdiqlash va history log'ga yozish"""
        order = self._orders.get(order_id)
        if order:
            order.status = OrderStatus.CONFIRMED
            self._notify_observers(order_id)
            
            item_names = [item.menu_item.name for item in order.items]
            self._history_log.add_order(
                order_id=order.order_id,
                table_number=order.table_number,
                staff_id=order.waiter_id,
                items=item_names,
                total=order.get_total()
            )
            return True
        return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Buyurtma olish"""
        return self._orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        """Barcha buyurtmalar"""
        return list(self._orders.values())
    
    def get_orders_by_table(self, table_number: int) -> List[Order]:
        """Stol bo'yicha buyurtmalar"""
        return [o for o in self._orders.values() if o.table_number == table_number]
    
    def get_orders_by_waiter(self, waiter_id: str) -> List[Order]:
        """Waiter bo'yicha buyurtmalar"""
        return [o for o in self._orders.values() if o.waiter_id == waiter_id]
    
    def attach_observer(self, order_id: str, observer):
        """Observer biriktirish"""
        subject = self._order_subjects.get(order_id)
        if subject:
            subject.attach(observer)
    
    def _notify_observers(self, order_id: str):
        """Kuzatuvchilarni xabardor qilish"""
        subject = self._order_subjects.get(order_id)
        if subject:
            subject.notify()
