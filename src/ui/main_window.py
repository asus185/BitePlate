import customtkinter as ctk
from models.staff import Role
from ui.table_view import TableView
from ui.order_panel import OrderPanel
from ui.kitchen_display import KitchenDisplay
from ui.dashboard import ManagerDashboard
from ui.billing_panel import BillingPanel

class MainWindow(ctk.CTk):
    """Asosiy oyna"""
    
    def __init__(self, user, services: dict):
        super().__init__()
        self._user = user
        self._services = services
        
        self.title(f"BitePlate - {user.name} ({user.role.value})")
        self.geometry("1200x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._setup_ui()
    
    def _setup_ui(self):
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        user_label = ctk.CTkLabel(sidebar, text=self._user.name, font=("Arial", 18, "bold"))
        user_label.pack(pady=(20, 5))
        
        role_label = ctk.CTkLabel(sidebar, text=self._user.role.value, text_color="gray")
        role_label.pack(pady=(0, 20))
        
        ctk.CTkLabel(sidebar, text="").pack(pady=10)
        
        if self._user.check_permission("view_tables"):
            ctk.CTkButton(sidebar, text="Tables", command=self._show_tables).pack(pady=5, padx=10, fill="x")
        
        if self._user.check_permission("take_orders"):
            ctk.CTkButton(sidebar, text="Orders", command=self._show_orders).pack(pady=5, padx=10, fill="x")
        
        if self._user.check_permission("manage_kitchen_queue"):
            ctk.CTkButton(sidebar, text="Kitchen", command=self._show_kitchen).pack(pady=5, padx=10, fill="x")
        
        if self._user.check_permission("view_bills"):
            ctk.CTkButton(sidebar, text="Billing", command=self._show_billing).pack(pady=5, padx=10, fill="x")
        
        if self._user.check_permission("view_reports"):
            ctk.CTkButton(sidebar, text="Reports", command=self._show_reports).pack(pady=5, padx=10, fill="x")
        
        ctk.CTkFrame(sidebar, height=2).pack(fill="x", padx=10, pady=20)
        
        logout_btn = ctk.CTkButton(sidebar, text="Logout", command=self.destroy, fg_color="red")
        logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")
        
        self._content_frame = ctk.CTkFrame(self)
        self._content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self._show_tables()
    
    def _clear_content(self):
        for widget in self._content_frame.winfo_children():
            widget.destroy()
    
    def _show_tables(self):
        self._clear_content()
        TableView(self._content_frame, self._services["table_service"])
    
    def _show_orders(self):
        self._clear_content()
        OrderPanel(self._content_frame, self._services, self._user)
    
    def _show_kitchen(self):
        self._clear_content()
        KitchenDisplay(self._content_frame, self._services["kitchen_service"], self._services["table_service"])
    
    def _show_billing(self):
        self._clear_content()
        BillingPanel(self._content_frame, self._services, self._user)
    
    def _show_reports(self):
        self._clear_content()
        ManagerDashboard(self._content_frame, self._services)
