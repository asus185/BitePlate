import customtkinter as ctk
from typing import Optional
from models.staff import Staff

class LoginWindow(ctk.CTk):
    """Login oynasi"""
    
    def __init__(self, auth_service):
        super().__init__()
        self._auth_service = auth_service
        self._authenticated_user: Optional[Staff] = None
        
        self.title("BitePlate - Login")
        self.geometry("400x500")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._setup_ui()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="BitePlate", font=("Arial", 32, "bold"))
        title.pack(pady=(40, 10))
        
        subtitle = ctk.CTkLabel(self, text="Smart Restaurant Management System", font=("Arial", 14))
        subtitle.pack(pady=(0, 30))
        
        username_label = ctk.CTkLabel(self, text="Username")
        username_label.pack(anchor="w", padx=40)
        
        self._username_entry = ctk.CTkEntry(self, width=320, placeholder_text="Enter username")
        self._username_entry.pack(pady=(5, 15), padx=40)
        
        password_label = ctk.CTkLabel(self, text="Password")
        password_label.pack(anchor="w", padx=40)
        
        self._password_entry = ctk.CTkEntry(self, width=320, placeholder_text="Enter password", show="*")
        self._password_entry.pack(pady=(5, 20), padx=40)
        
        login_btn = ctk.CTkButton(self, text="Login", command=self._handle_login, width=320, height=40)
        login_btn.pack(pady=10)
        
        self._error_label = ctk.CTkLabel(self, text="", text_color="red")
        self._error_label.pack(pady=10)
        
        info = ctk.CTkLabel(
            self, 
            text="Default: manager/admin123 | chef/chef123 | waiter/waiter123 | cashier/cashier123",
            font=("Arial", 10),
            text_color="gray"
        )
        info.pack(pady=(20, 10))
    
    def _handle_login(self):
        username = self._username_entry.get()
        password = self._password_entry.get()
        
        if not username or not password:
            self._error_label.configure(text="Please enter both username and password")
            return
        
        user = self._auth_service.authenticate(username, password)
        
        if user:
            self._authenticated_user = user
            self.destroy()
        else:
            self._error_label.configure(text="Invalid username or password")
    
    def get_authenticated_user(self) -> Optional[Staff]:
        self.wait_window()
        return self._authenticated_user
