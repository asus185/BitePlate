from typing import List, Optional, Dict
from models.table import Table, TableStatus

class TableService:
    """Stol boshqaruv xizmati"""
    
    def __init__(self):
        self._tables: Dict[int, Table] = {}
    
    def add_table(self, table_number: int, capacity: int, location: str = "Main Hall") -> Table:
        """Yangi stol qo'shish"""
        table = Table(table_number, capacity, location)
        self._tables[table_number] = table
        return table
    
    def get_table(self, table_number: int) -> Optional[Table]:
        """Stol olish"""
        return self._tables.get(table_number)
    
    def get_all_tables(self) -> List[Table]:
        """Barcha stollar"""
        return list(self._tables.values())
    
    def get_available_tables(self) -> List[Table]:
        """Bo'sh stollar"""
        return [t for t in self._tables.values() if t.status == TableStatus.FREE]
    
    def get_tables_by_status(self, status: TableStatus) -> List[Table]:
        """Status bo'yicha stollar"""
        return [t for t in self._tables.values() if t.status == status]
    
    def occupy_table(self, table_number: int, order_id: str) -> bool:
        """Stolni egallash"""
        table = self._tables.get(table_number)
        if table:
            return table.occupy(order_id)
        return False
    
    def reserve_table(self, table_number: int, reservation_id: str) -> bool:
        """Stolni band qilish"""
        table = self._tables.get(table_number)
        if table:
            return table.reserve(reservation_id)
        return False
    
    def await_bill(self, table_number: int) -> bool:
        """Bill kutilmoqda"""
        table = self._tables.get(table_number)
        if table:
            return table.await_bill()
        return False
    
    def clear_table(self, table_number: int) -> bool:
        """Stolni tozalash"""
        table = self._tables.get(table_number)
        if table:
            return table.clear()
        return False
    
    def free_table(self, table_number: int) -> bool:
        """Stolni bo'shatish"""
        table = self._tables.get(table_number)
        if table:
            return table.free_up()
        return False
