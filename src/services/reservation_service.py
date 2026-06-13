from typing import List, Optional, Dict
from datetime import datetime
from models.reservation import Reservation

class ReservationService:
    """Bron qilish xizmati"""
    
    def __init__(self):
        self._reservations: Dict[str, Reservation] = {}
        self._next_reservation_id = 1
    
    def create_reservation(self, customer_name: str, phone: str, 
                          table_number: int, date: datetime, 
                          party_size: int, special_requests: str = "") -> Reservation:
        """Yangi bron yaratish"""
        reservation_id = f"RES-{self._next_reservation_id:04d}"
        self._next_reservation_id += 1
        
        reservation = Reservation(
            reservation_id, customer_name, phone, 
            table_number, date, party_size, special_requests
        )
        self._reservations[reservation_id] = reservation
        return reservation
    
    def confirm_reservation(self, reservation_id: str) -> bool:
        """Bronni tasdiqlash"""
        reservation = self._reservations.get(reservation_id)
        if reservation:
            reservation.confirm()
            return True
        return False
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """Bronni bekor qilish"""
        reservation = self._reservations.get(reservation_id)
        if reservation:
            reservation.cancel()
            return True
        return False
    
    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Bron olish"""
        return self._reservations.get(reservation_id)
    
    def get_all_reservations(self) -> List[Reservation]:
        """Barcha bronlar"""
        return list(self._reservations.values())
    
    def get_reservations_by_date(self, date: datetime) -> List[Reservation]:
        """Sana bo'yicha bronlar"""
        return [
            r for r in self._reservations.values()
            if r.date.date() == date.date()
        ]
    
    def get_reservations_by_table(self, table_number: int) -> List[Reservation]:
        """Stol bo'yicha bronlar"""
        return [r for r in self._reservations.values() if r.table_number == table_number]
