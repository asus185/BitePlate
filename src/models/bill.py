from typing import List, Optional
from datetime import datetime

class BillLineItem:
    """Bill elementi"""
    
    def __init__(self, item_name: str, quantity: int, unit_price: float, total_price: float):
        self._item_name = item_name
        self._quantity = quantity
        self._unit_price = unit_price
        self._total_price = total_price
    
    @property
    def item_name(self) -> str:
        return self._item_name
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @property
    def unit_price(self) -> float:
        return self._unit_price
    
    @property
    def total_price(self) -> float:
        return self._total_price
    
    def __str__(self) -> str:
        return f"{self._item_name} x{self._quantity} @ ${self._unit_price:.2f} = ${self._total_price:.2f}"

class Bill:
    """Hisob (Bill)"""
    
    TAX_RATE = 0.10
    
    def __init__(self, bill_id: str, order_id: str, table_number: int):
        self._bill_id = bill_id
        self._order_id = order_id
        self._table_number = table_number
        self._line_items: List[BillLineItem] = []
        self._subtotal = 0.0
        self._tax = 0.0
        self._tip = 0.0
        self._discount = 0.0
        self._total = 0.0
        self._created_at = datetime.now()
        self._paid = False
        self._payment_method: Optional[str] = None
    
    @property
    def bill_id(self) -> str:
        return self._bill_id
    
    @property
    def order_id(self) -> str:
        return self._order_id
    
    @property
    def table_number(self) -> int:
        return self._table_number
    
    @property
    def line_items(self) -> List[BillLineItem]:
        return self._line_items.copy()
    
    @property
    def subtotal(self) -> float:
        return self._subtotal
    
    @property
    def tax(self) -> float:
        return self._tax
    
    @property
    def tip(self) -> float:
        return self._tip
    
    @property
    def total(self) -> float:
        return self._total
    
    @property
    def paid(self) -> bool:
        return self._paid
    
    def add_item(self, item_name: str, quantity: int, unit_price: float):
        """Bill'ga element qo'shish"""
        total_price = quantity * unit_price
        line_item = BillLineItem(item_name, quantity, unit_price, total_price)
        self._line_items.append(line_item)
        self._recalculate()
    
    def set_discount(self, discount: float):
        """Chegirma o'rnatish"""
        self._discount = discount
        self._recalculate()
    
    def set_tip(self, tip: float):
        """Baxshish qo'shish"""
        self._tip = tip
        self._recalculate()
    
    def mark_paid(self, payment_method: str):
        """To'langan deb belgilash"""
        self._paid = True
        self._payment_method = payment_method
    
    def _recalculate(self):
        """Qayta hisoblash"""
        self._subtotal = sum(item.total_price for item in self._line_items) - self._discount
        self._tax = self._subtotal * Bill.TAX_RATE
        self._total = self._subtotal + self._tax + self._tip
    
    def split_bill(self, num_people: int) -> float:
        """Bill'ni bo'lish"""
        if num_people < 1:
            raise ValueError("Number of people must be at least 1")
        return self._total / num_people
    
    def generate_receipt(self) -> str:
        """Chek generatsiya qilish"""
        receipt = f"{'='*40}\n"
        receipt += f"  BITEPLATE RESTAURANT\n"
        receipt += f"  Bill #{self._bill_id}\n"
        receipt += f"  Table {self._table_number}\n"
        receipt += f"  {self._created_at.strftime('%Y-%m-%d %H:%M')}\n"
        receipt += f"{'='*40}\n\n"
        
        for item in self._line_items:
            receipt += f"  {item}\n"
        
        receipt += f"\n{'-'*40}\n"
        receipt += f"  Subtotal: ${self._subtotal:.2f}\n"
        if self._discount > 0:
            receipt += f"  Discount: -${self._discount:.2f}\n"
        receipt += f"  Tax (10%): ${self._tax:.2f}\n"
        if self._tip > 0:
            receipt += f"  Tip: ${self._tip:.2f}\n"
        receipt += f"  TOTAL: ${self._total:.2f}\n"
        receipt += f"{'='*40}\n"
        
        if self._paid:
            receipt += f"  PAID via {self._payment_method}\n"
        
        return receipt
    
    def __str__(self) -> str:
        return f"Bill #{self._bill_id} | Table {self._table_number} | ${self._total:.2f}"
