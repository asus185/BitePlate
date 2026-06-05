import customtkinter as ctk
from models.menu_item import Starter, MainCourse, Dessert, Beverage
from models.order import OrderStatus

class OrderPanel(ctk.CTkFrame):
    """Buyurtma paneli"""
    
    def __init__(self, master, services, current_user=None):
        super().__init__(master)
        self._services = services
        self._current_user = current_user
        self._current_order = None
        self._menu_items = []
        self.pack(fill="both", expand=True)
        
        self._setup_ui()
        self._load_sample_menu()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="Order Management", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        menu_frame = ctk.CTkFrame(main_frame)
        menu_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 18, "bold")).pack(pady=10)
        
        self._menu_list = ctk.CTkScrollableFrame(menu_frame)
        self._menu_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        order_frame = ctk.CTkFrame(main_frame)
        order_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(order_frame, text="Current Order", font=("Arial", 18, "bold")).pack(pady=10)
        
        self._order_list = ctk.CTkScrollableFrame(order_frame)
        self._order_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        self._total_label = ctk.CTkLabel(order_frame, text="Total: $0.00", font=("Arial", 16, "bold"))
        self._total_label.pack(pady=10)
        
        btn_frame = ctk.CTkFrame(order_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="New Order", command=self._new_order).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(btn_frame, text="Confirm Order", command=self._confirm_order).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(btn_frame, text="Clear", command=self._clear_order, fg_color="red").pack(side="left", padx=5, fill="x", expand=True)
    
    def _load_sample_menu(self):
        self._menu_items = [
            Starter("S001", "Caesar Salad", 8.99, "Fresh romaine lettuce with parmesan"),
            Starter("S002", "Soup of the Day", 6.99, "Chef's daily special"),
            MainCourse("M001", "Grilled Steak", 24.99, "Premium beef steak", spiciness=1),
            MainCourse("M002", "Pasta Carbonara", 18.99, "Classic Italian pasta"),
            MainCourse("M003", "Fish & Chips", 16.99, "Beer-battered cod"),
            Dessert("D001", "Chocolate Cake", 7.99, "Rich dark chocolate"),
            Dessert("D002", "Ice Cream", 5.99, "Vanilla, chocolate, or strawberry"),
            Beverage("B001", "Soft Drink", 2.99, size="Medium"),
            Beverage("B002", "Fresh Juice", 4.99, size="Large"),
            Beverage("B003", "Wine", 12.99, size="Glass", is_alcoholic=True),
        ]
        
        for item in self._menu_items:
            frame = ctk.CTkFrame(self._menu_list)
            frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame, text=f"{item.name}").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=f"${item.get_price():.2f}").pack(side="left", padx=5)
            
            add_btn = ctk.CTkButton(frame, text="+ Add", width=60, 
                                   command=lambda i=item: self._add_to_order(i))
            add_btn.pack(side="right", padx=5)
    
    def _new_order(self):
        tables = self._services["table_service"].get_available_tables()
        if not tables:
            from ui.components.dialogs import CustomDialog
            CustomDialog("Error", "No available tables!", self).wait()
            return
        
        waiter_id = self._current_user.staff_id if self._current_user else "W001"
        self._current_order = self._services["order_service"].create_order(tables[0].table_number, waiter_id)
        self._services["table_service"].occupy_table(tables[0].table_number, self._current_order.order_id)
        self._refresh_order_display()
    
    def _add_to_order(self, menu_item):
        if not self._current_order:
            self._new_order()
            if not self._current_order:
                return
        
        self._services["order_service"].add_item_to_order(
            self._current_order.order_id, menu_item, 1
        )
        self._refresh_order_display()
    
    def _confirm_order(self):
        if self._current_order and self._current_order.items:
            self._services["order_service"].confirm_order(self._current_order.order_id)
            
            kitchen_service = self._services.get("kitchen_service")
            if kitchen_service:
                kitchen_service.add_order_to_queue(self._current_order)
            
            from ui.components.dialogs import CustomDialog
            CustomDialog("Success", f"Order {self._current_order.order_id} confirmed!", self).wait()
            
            self._current_order = None
            self._refresh_order_display()
    
    def _clear_order(self):
        self._current_order = None
        self._refresh_order_display()
    
    def _refresh_order_display(self):
        for widget in self._order_list.winfo_children():
            widget.destroy()
        
        if self._current_order:
            ctk.CTkLabel(self._order_list, text=f"Order #{self._current_order.order_id} | Table {self._current_order.table_number}").pack(fill="x", pady=5)
            
            for item in self._current_order.items:
                ctk.CTkLabel(self._order_list, text=str(item)).pack(fill="x", pady=2)
            
            self._total_label.configure(text=f"Total: ${self._current_order.get_total():.2f}")
        else:
            ctk.CTkLabel(self._order_list, text="No active order", text_color="gray").pack(pady=20)
            self._total_label.configure(text="Total: $0.00")
