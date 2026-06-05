import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from config import DEFAULT_STAFF
from models.staff import Manager, HeadChef, Waiter, Cashier, Role
from services.table_service import TableService
from services.order_service import OrderService
from services.kitchen_service import KitchenService
from services.billing_service import BillingService
from services.reservation_service import ReservationService
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

ROLE_MAP = {
    "manager": Manager,
    "chef": HeadChef,
    "waiter": Waiter,
    "cashier": Cashier,
}

class AuthService:
    """Autentifikatsiya xizmati"""
    
    def __init__(self):
        self._users = {}
        self._setup_default_users()
    
    def _setup_default_users(self):
        """Default foydalanuvchilarni config'dan yaratish"""
        for key, user_data in DEFAULT_STAFF.items():
            role_class = ROLE_MAP[user_data["role"]]
            self._users[user_data["username"]] = role_class(
                staff_id=user_data["staff_id"],
                username=user_data["username"],
                password=user_data["password"],
                name=user_data["name"]
            )
    
    def authenticate(self, username: str, password: str):
        """Login tekshirish"""
        user = self._users.get(username)
        if user and user.authenticate(password):
            return user
        return None

class BitePlateApp:
    """Asosiy application"""
    
    def __init__(self):
        self._auth_service = AuthService()
        self._services = {
            "table_service": TableService(),
            "order_service": OrderService(),
            "kitchen_service": KitchenService(),
            "billing_service": BillingService(),
            "reservation_service": ReservationService(),
        }
        self._setup_sample_data()
    
    def _setup_sample_data(self):
        """Namuna stollar yaratish"""
        table_service = self._services["table_service"]
        for i in range(1, 11):
            capacity = 2 if i <= 4 else 4 if i <= 8 else 6
            table_service.add_table(i, capacity)
    
    def run(self):
        """Application ishga tushirish"""
        login_window = LoginWindow(self._auth_service)
        user = login_window.get_authenticated_user()
        
        if user:
            main_window = MainWindow(user, self._services)
            main_window.mainloop()

if __name__ == "__main__":
    app = BitePlateApp()
    app.run()
