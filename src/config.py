"""BitePlate Configuration - Environment variables for sensitive values"""
import os

def _env(key: str, default: str) -> str:
    """Environment variable o'qish, default qiymat bilan"""
    return os.environ.get(key, default)

DEFAULT_STAFF = {
    "manager": {
        "staff_id": "M001",
        "username": "manager",
        "password": _env("BITEPLATE_MANAGER_PASSWORD", "admin123"),
        "name": "John Manager",
        "role": "manager"
    },
    "chef": {
        "staff_id": "C001",
        "username": "chef",
        "password": _env("BITEPLATE_CHEF_PASSWORD", "chef123"),
        "name": "Chef Gordon",
        "role": "chef"
    },
    "waiter": {
        "staff_id": "W001",
        "username": "waiter",
        "password": _env("BITEPLATE_WAITER_PASSWORD", "waiter123"),
        "name": "Waiter Sarah",
        "role": "waiter"
    },
    "cashier": {
        "staff_id": "CA001",
        "username": "cashier",
        "password": _env("BITEPLATE_CASHIER_PASSWORD", "cashier123"),
        "name": "Cashier Mike",
        "role": "cashier"
    }
}

TAX_RATE = 0.10
TABLE_COUNT = 10
