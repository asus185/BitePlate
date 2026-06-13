import customtkinter as ctk
from models.bill import Bill
from models.order import OrderStatus
from patterns.strategy import StandardPricing, HappyHourPricing, LoyaltyCardPricing, WeekendSurchargePricing

class BillingPanel(ctk.CTkFrame):
    """Billing panel - Bill generatsiya, to'lov, chegirma"""
    
    def __init__(self, master, services, current_user=None):
        super().__init__(master)
        self._services = services
        self._current_user = current_user
        self._current_bill = None
        self.pack(fill="both", expand=True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="Billing & POS", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(left_frame, text="Pending Bills", font=("Arial", 16, "bold")).pack(pady=10)
        
        self._bills_list = ctk.CTkScrollableFrame(left_frame)
        self._bills_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(right_frame, text="Bill Details", font=("Arial", 16, "bold")).pack(pady=10)
        
        self._bill_detail_frame = ctk.CTkScrollableFrame(right_frame)
        self._bill_detail_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self._total_label = ctk.CTkLabel(right_frame, text="Total: $0.00", font=("Arial", 18, "bold"))
        self._total_label.pack(pady=10)
        
        strategy_frame = ctk.CTkFrame(right_frame)
        strategy_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(strategy_frame, text="Pricing Strategy:").pack(pady=5)
        
        self._strategy_var = ctk.StringVar(value="Standard")
        strategies = [
            ("Standard", StandardPricing()),
            ("Happy Hour (-20%)", HappyHourPricing()),
            ("Loyalty Card (-10%)", LoyaltyCardPricing()),
            ("Weekend (+10%)", WeekendSurchargePricing()),
        ]
        for label, _ in strategies:
            ctk.CTkRadioButton(strategy_frame, text=label, variable=self._strategy_var,
                              value=label, command=self._apply_strategy).pack(anchor="w", padx=10)
        
        btn_frame = ctk.CTkFrame(right_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Generate Bill", command=self._generate_bill).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(btn_frame, text="Apply Tip", command=self._apply_tip).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(btn_frame, text="Split Bill", command=self._split_bill).pack(side="left", padx=5, fill="x", expand=True)
        
        pay_frame = ctk.CTkFrame(right_frame)
        pay_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(pay_frame, text="Pay - Cash", command=lambda: self._pay("Cash"), fg_color="#2ecc71").pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(pay_frame, text="Pay - Card", command=lambda: self._pay("Card"), fg_color="#3498db").pack(side="left", padx=5, fill="x", expand=True)
        
        self._receipt_frame = ctk.CTkTextbox(right_frame, height=150, state="disabled")
        self._receipt_frame.pack(fill="x", padx=10, pady=10)
        
        self._refresh_bills()
    
    def _generate_bill(self):
        """Order'dan bill yaratish"""
        orders = self._services["order_service"].get_all_orders()
        unpaid_orders = [o for o in orders if o.status in [OrderStatus.SERVED, OrderStatus.READY]]
        
        if not unpaid_orders:
            from ui.components.dialogs import CustomDialog
            CustomDialog("Info", "No orders ready for billing!", self).wait()
            return
        
        order = unpaid_orders[0]
        bill = self._services["billing_service"].create_bill(order)
        self._current_bill = bill
        self._refresh_bills()
        self._show_bill_detail(bill)
    
    def _refresh_bills(self):
        """Bill'lar ro'yxatini yangilash"""
        for widget in self._bills_list.winfo_children():
            widget.destroy()
        
        bills = self._services["billing_service"].get_all_bills()
        if not bills:
            ctk.CTkLabel(self._bills_list, text="No bills yet", text_color="gray").pack(pady=20)
            return
        
        for bill in bills:
            card = ctk.CTkFrame(self._bills_list)
            card.pack(fill="x", pady=3, padx=5)
            
            status_color = "#2ecc71" if bill.paid else "#f39c12"
            status_text = "PAID" if bill.paid else "PENDING"
            
            ctk.CTkLabel(card, text=f"Bill #{bill.bill_id} | Table {bill.table_number}").pack(side="left", padx=5)
            ctk.CTkLabel(card, text=f"${bill.total:.2f}", font=("Arial", 12, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(card, text=status_text, fg_color=status_color,
                        text_color="white", corner_radius=5, padx=8, pady=3).pack(side="right", padx=5)
            
            if not bill.paid:
                ctk.CTkButton(card, text="View", width=50,
                             command=lambda b=bill: self._show_bill_detail(b)).pack(side="right", padx=3)
    
    def _show_bill_detail(self, bill):
        """Bill tafsilotlarini ko'rsatish"""
        for widget in self._bill_detail_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self._bill_detail_frame, text=f"Bill #{bill.bill_id}", font=("Arial", 14, "bold")).pack(fill="x", pady=5)
        ctk.CTkLabel(self._bill_detail_frame, text=f"Order: {bill.order_id}").pack(fill="x")
        ctk.CTkLabel(self._bill_detail_frame, text=f"Table: {bill.table_number}").pack(fill="x")
        
        ctk.CTkLabel(self._bill_detail_frame, text="").pack(pady=5)
        
        for item in bill.line_items:
            ctk.CTkLabel(self._bill_detail_frame, text=str(item)).pack(fill="x", pady=2)
        
        ctk.CTkLabel(self._bill_detail_frame, text="").pack(pady=5)
        ctk.CTkLabel(self._bill_detail_frame, text=f"Subtotal: ${bill.subtotal:.2f}").pack(fill="x")
        if bill._discount > 0:
            ctk.CTkLabel(self._bill_detail_frame, text=f"Discount: -${bill._discount:.2f}", text_color="#e74c3c").pack(fill="x")
        ctk.CTkLabel(self._bill_detail_frame, text=f"Tax (10%): ${bill.tax:.2f}").pack(fill="x")
        if bill.tip > 0:
            ctk.CTkLabel(self._bill_detail_frame, text=f"Tip: ${bill.tip:.2f}").pack(fill="x")
        
        self._total_label.configure(text=f"TOTAL: ${bill.total:.2f}")
    
    def _apply_strategy(self):
        """Pricing strategiyasini qo'llash"""
        if not self._current_bill:
            return
        
        strategy_map = {
            "Standard": StandardPricing(),
            "Happy Hour (-20%)": HappyHourPricing(),
            "Loyalty Card (-10%)": LoyaltyCardPricing(),
            "Weekend (+10%)": WeekendSurchargePricing(),
        }
        
        strategy = strategy_map.get(self._strategy_var.get(), StandardPricing())
        self._services["billing_service"].pricing_engine.strategy = strategy
        
        bill_id = self._current_bill.bill_id
        self._services["billing_service"].calculate_total(bill_id)
        self._show_bill_detail(self._current_bill)
    
    def _apply_tip(self):
        """Baxshish qo'shish"""
        if not self._current_bill:
            return
        
        tip_window = ctk.CTkToplevel(self)
        tip_window.title("Add Tip")
        tip_window.geometry("300x150")
        tip_window.grab_set()
        
        ctk.CTkLabel(tip_window, text="Tip Amount ($):").pack(pady=10)
        tip_entry = ctk.CTkEntry(tip_window, width=200)
        tip_entry.pack(pady=5)
        
        def confirm_tip():
            try:
                tip = float(tip_entry.get())
                if tip < 0:
                    raise ValueError
                self._services["billing_service"].set_tip(self._current_bill.bill_id, tip)
                self._show_bill_detail(self._current_bill)
                tip_window.destroy()
            except ValueError:
                ctk.CTkLabel(tip_window, text="Invalid amount!", text_color="red").pack()
        
        ctk.CTkButton(tip_window, text="Apply", command=confirm_tip).pack(pady=10)
    
    def _split_bill(self):
        """Bill'ni bo'lish"""
        if not self._current_bill:
            return
        
        split_window = ctk.CTkToplevel(self)
        split_window.title("Split Bill")
        split_window.geometry("300x180")
        split_window.grab_set()
        
        ctk.CTkLabel(split_window, text="Number of people:").pack(pady=10)
        people_entry = ctk.CTkEntry(split_window, width=200)
        people_entry.pack(pady=5)
        
        result_label = ctk.CTkLabel(split_window, text="", font=("Arial", 14, "bold"))
        result_label.pack(pady=5)
        
        def calculate_split():
            try:
                people = int(people_entry.get())
                per_person = self._services["billing_service"].split_bill(self._current_bill.bill_id, people)
                result_label.configure(text=f"${per_person:.2f} per person")
            except (ValueError, ZeroDivisionError):
                result_label.configure(text="Invalid number!", text_color="red")
        
        ctk.CTkButton(split_window, text="Calculate", command=calculate_split).pack(pady=10)
    
    def _pay(self, method):
        """To'lov qilish"""
        if not self._current_bill or self._current_bill.paid:
            from ui.components.dialogs import CustomDialog
            CustomDialog("Error", "No pending bill to pay!", self).wait()
            return
        
        self._services["billing_service"].close_bill(self._current_bill.bill_id, method)
        
        receipt = self._services["billing_service"].generate_receipt(self._current_bill.bill_id)
        self._receipt_frame.configure(state="normal")
        self._receipt_frame.delete("1.0", "end")
        self._receipt_frame.insert("1.0", receipt)
        self._receipt_frame.configure(state="disabled")
        
        self._services["table_service"].await_bill(self._current_bill.table_number)
        self._services["table_service"].clear_table(self._current_bill.table_number)
        self._services["table_service"].free_table(self._current_bill.table_number)
        
        self._refresh_bills()
        self._show_bill_detail(self._current_bill)
