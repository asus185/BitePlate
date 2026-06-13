from typing import Optional, Dict, List
from models.bill import Bill
from patterns.strategy import PricingEngine, StandardPricing

class BillingService:
    """Billing xizmati"""
    
    def __init__(self):
        self._bills: Dict[str, Bill] = {}
        self._pricing_engine = PricingEngine()
        self._next_bill_id = 1
    
    @property
    def pricing_engine(self) -> PricingEngine:
        return self._pricing_engine
    
    def create_bill(self, order) -> Bill:
        """Order'dan yangi bill yaratish"""
        bill_id = f"BILL-{self._next_bill_id:04d}"
        self._next_bill_id += 1
        
        bill = Bill(bill_id, order.order_id, order.table_number)
        
        for item in order.items:
            bill.add_item(
                item.menu_item.name,
                item.quantity,
                item.menu_item.get_price()
            )
        
        self._bills[bill_id] = bill
        return bill
    
    def calculate_total(self, bill_id: str) -> float:
        """Pricing strategiyasi bilan total hisoblash"""
        bill = self._bills.get(bill_id)
        if bill:
            discounted_total = self._pricing_engine.calculate_total(bill)
            bill._discount = bill.subtotal - discounted_total
            bill._recalculate()
            return discounted_total
        return 0.0
    
    def set_tip(self, bill_id: str, tip: float) -> bool:
        """Baxshish qo'shish"""
        bill = self._bills.get(bill_id)
        if bill:
            bill.set_tip(tip)
            return True
        return False
    
    def close_bill(self, bill_id: str, payment_method: str) -> bool:
        """Bill'ni yopish"""
        bill = self._bills.get(bill_id)
        if bill:
            bill.mark_paid(payment_method)
            return True
        return False
    
    def get_bill(self, bill_id: str) -> Optional[Bill]:
        """Bill olish"""
        return self._bills.get(bill_id)
    
    def get_all_bills(self) -> List[Bill]:
        """Barcha bill'lar"""
        return list(self._bills.values())
    
    def generate_receipt(self, bill_id: str) -> Optional[str]:
        """Chek generatsiya qilish"""
        bill = self._bills.get(bill_id)
        if bill:
            return bill.generate_receipt()
        return None
    
    def split_bill(self, bill_id: str, num_people: int) -> Optional[float]:
        """Bill'ni bo'lish"""
        bill = self._bills.get(bill_id)
        if bill:
            return bill.split_bill(num_people)
        return None
    
    def get_bills_for_table(self, table_number: int) -> List[Bill]:
        """Stol bo'yicha bill'lar"""
        return [b for b in self._bills.values() if b.table_number == table_number]
