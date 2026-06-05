class BitePlateException(Exception):
    """Asosiy exception"""
    pass

class OrderNotFoundException(BitePlateException):
    """Buyurtma topilmadi"""
    pass

class TableNotAvailableException(BitePlateException):
    """Stol bo'sh emas"""
    pass

class PermissionDeniedException(BitePlateException):
    """Ruxsat yo'q"""
    pass

class InvalidOrderStateException(BitePlateException):
    """Buyurtma holati noto'g'ri"""
    pass
