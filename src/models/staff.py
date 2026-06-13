from abc import ABC, abstractmethod
from enum import Enum

class Role(Enum):
    """Xodim rollari"""
    MANAGER = "Manager"
    HEAD_CHEF = "Head Chef"
    WAITER = "Waiter"
    CASHIER = "Cashier"

class Staff(ABC):
    """Asosiy xodim class"""
    
    def __init__(self, staff_id: str, username: str, password: str, name: str, role: Role):
        self._staff_id = staff_id
        self._username = username
        self._password = password
        self._name = name
        self._role = role
        self._permissions = self._get_default_permissions()
    
    @property
    def staff_id(self) -> str:
        return self._staff_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def role(self) -> Role:
        return self._role
    
    @property
    def permissions(self) -> dict:
        return self._permissions.copy()
    
    def _get_default_permissions(self) -> dict:
        """Default permissions"""
        return {
            "view_tables": False,
            "take_orders": False,
            "modify_orders": False,
            "view_kitchen_queue": False,
            "manage_kitchen_queue": False,
            "view_bills": False,
            "close_bills": False,
            "view_reports": False,
            "manage_staff": False,
        }
    
    def check_permission(self, permission: str) -> bool:
        """Permission tekshirish"""
        return self._permissions.get(permission, False)
    
    def authenticate(self, password: str) -> bool:
        """Login tekshirish"""
        return self._password == password
    
    @abstractmethod
    def get_dashboard_view(self) -> str:
        """Har bir rol uchun alohida dashboard"""
        pass
    
    def __str__(self) -> str:
        return f"{self._name} ({self._role.value})"

class Manager(Staff):
    """Manager - hamma narsaga ruxsat"""
    
    def __init__(self, staff_id: str, username: str, password: str, name: str):
        super().__init__(staff_id, username, password, name, Role.MANAGER)
        self._permissions = {
            "view_tables": True, "take_orders": True, "modify_orders": True,
            "view_kitchen_queue": True, "manage_kitchen_queue": True,
            "view_bills": True, "close_bills": True, "view_reports": True,
            "manage_staff": True,
        }
    
    def get_dashboard_view(self) -> str:
        return "Manager Dashboard - Full Access"

class HeadChef(Staff):
    """Head Chef - Kitchen boshqaruvi"""
    
    def __init__(self, staff_id: str, username: str, password: str, name: str):
        super().__init__(staff_id, username, password, name, Role.HEAD_CHEF)
        self._permissions = {
            "view_tables": False, "take_orders": False, "modify_orders": False,
            "view_kitchen_queue": True, "manage_kitchen_queue": True,
            "view_bills": False, "close_bills": False, "view_reports": False,
            "manage_staff": False,
        }
    
    def get_dashboard_view(self) -> str:
        return "Kitchen Dashboard - Order Queue Management"

class Waiter(Staff):
    """Waiter - Buyurtma olish"""
    
    def __init__(self, staff_id: str, username: str, password: str, name: str):
        super().__init__(staff_id, username, password, name, Role.WAITER)
        self._permissions = {
            "view_tables": True, "take_orders": True, "modify_orders": True,
            "view_kitchen_queue": True, "manage_kitchen_queue": False,
            "view_bills": True, "close_bills": False, "view_reports": False,
            "manage_staff": False,
        }
    
    def get_dashboard_view(self) -> str:
        return "Waiter Dashboard - Table & Order Management"

class Cashier(Staff):
    """Cashier - Billing"""
    
    def __init__(self, staff_id: str, username: str, password: str, name: str):
        super().__init__(staff_id, username, password, name, Role.CASHIER)
        self._permissions = {
            "view_tables": True, "take_orders": False, "modify_orders": False,
            "view_kitchen_queue": False, "manage_kitchen_queue": False,
            "view_bills": True, "close_bills": True, "view_reports": False,
            "manage_staff": False,
        }
    
    def get_dashboard_view(self) -> str:
        return "Cashier Dashboard - Billing & Payments"
