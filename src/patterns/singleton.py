from typing import List, Optional, Dict
from datetime import datetime, timedelta

class OrderHistoryLog:
    """Singleton Pattern - Buyurtmalar tarixi logi"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._logs: List[Dict] = []
        self._initialized = True
    
    def add_order(self, order_id: str, table_number: int, staff_id: str, 
                  items: List[str], total: float, timestamp: Optional[datetime] = None):
        """Buyurtmani log'ga qo'shish"""
        log_entry = {
            "order_id": order_id,
            "table_number": table_number,
            "staff_id": staff_id,
            "items": items,
            "total": total,
            "timestamp": timestamp or datetime.now()
        }
        self._logs.append(log_entry)
    
    def get_all_orders(self) -> List[Dict]:
        """Barcha buyurtmalarni olish"""
        return self._logs.copy()
    
    def get_orders_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Sana bo'yicha filtrlash"""
        return [
            log for log in self._logs
            if start_date <= log["timestamp"] <= end_date
        ]
    
    def get_orders_by_table(self, table_number: int) -> List[Dict]:
        """Stol bo'yicha filtrlash"""
        return [log for log in self._logs if log["table_number"] == table_number]
    
    def get_most_frequent_item(self) -> Optional[str]:
        """Eng ko'p buyurtma qilingan taom"""
        if not self._logs:
            return None
        
        item_counts = {}
        for log in self._logs:
            for item in log["items"]:
                item_counts[item] = item_counts.get(item, 0) + 1
        
        return max(item_counts, key=item_counts.get) if item_counts else None
    
    def get_total_revenue(self) -> float:
        """Umumiy daromad"""
        return sum(log["total"] for log in self._logs)
    
    def get_peak_hours(self) -> Dict[int, int]:
        """Eng band soatlar"""
        hour_counts = {}
        for log in self._logs:
            hour = log["timestamp"].hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        return hour_counts
    
    def clear_logs(self):
        """Log'larni tozalash (test uchun)"""
        self._logs.clear()
