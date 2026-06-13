from datetime import datetime

class Reservation:
    """Bron qilish"""
    
    def __init__(self, reservation_id: str, customer_name: str, phone: str,
                 table_number: int, date: datetime, party_size: int, special_requests: str = ""):
        self._reservation_id = reservation_id
        self._customer_name = customer_name
        self._phone = phone
        self._table_number = table_number
        self._date = date
        self._party_size = party_size
        self._special_requests = special_requests
        self._confirmed = False
        self._created_at = datetime.now()
    
    @property
    def reservation_id(self) -> str:
        return self._reservation_id
    
    @property
    def customer_name(self) -> str:
        return self._customer_name
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @property
    def table_number(self) -> int:
        return self._table_number
    
    @property
    def date(self) -> datetime:
        return self._date
    
    @property
    def party_size(self) -> int:
        return self._party_size
    
    @property
    def special_requests(self) -> str:
        return self._special_requests
    
    @property
    def confirmed(self) -> bool:
        return self._confirmed
    
    def confirm(self):
        """Tasdiqlash"""
        self._confirmed = True
    
    def cancel(self):
        """Bekor qilish"""
        self._confirmed = False
    
    def __str__(self) -> str:
        status = "Confirmed" if self._confirmed else "Pending"
        return f"Reservation #{self._reservation_id} | {self._customer_name} | Table {self._table_number} | {self._date.strftime('%Y-%m-%d %H:%M')} | {status}"
