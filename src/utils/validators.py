def validate_positive_number(value: float, name: str = "Value") -> bool:
    """Musbat sonni tekshirish"""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return True

def validate_non_empty_string(value: str, name: str = "Value") -> bool:
    """Bo'sh bo'lmagan satrni tekshirish"""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} cannot be empty")
    return True

def validate_quantity(quantity: int) -> bool:
    """Miqdorni tekshirish"""
    if not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    return True

def validate_table_number(table_number: int) -> bool:
    """Stol raqamini tekshirish"""
    if not isinstance(table_number, int):
        raise ValueError("Table number must be an integer")
    if table_number < 1:
        raise ValueError("Table number must be at least 1")
    return True
