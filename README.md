# BitePlate - Smart Restaurant Management System

## Overview
BitePlate is a modern restaurant management system built using Object-Oriented Programming principles and industry-recognized design patterns. It replaces paper-based and legacy processes with a maintainable, scalable software solution.

## Language & IDE Justification
- **Language:** Python 3.10+ — Chosen for its readability, extensive standard library, and strong OOP support. Python's dynamic typing allows for flexible pattern implementations while maintaining clean, readable code.
- **IDE:** VS Code — Lightweight, excellent Python support, integrated terminal, and Git integration.
- **UI Framework:** CustomTkinter — Modern, customizable GUI toolkit built on tkinter, providing a professional dark-mode interface.

## Features
- Table Management (Free → Reserved → Occupied → Awaiting Bill → Cleared)
- Reservation System with confirmation
- Order Management with modification capabilities
- Kitchen Queue with Command Pattern (execute/undo)
- Pricing Engine with Strategy Pattern (runtime strategy swapping)
- Order Notifications with Observer Pattern
- Order History Log with Singleton Pattern
- Role-based access control (Manager, Head Chef, Waiter, Cashier)
- Billing & POS with tip, split bill, and receipt generation
- Secure coding practices (config-based credentials, input validation, custom exceptions)

## Design Patterns Implemented
1. **Singleton** — OrderHistoryLog (globally accessible order log)
2. **Command** — KitchenQueue (execute/undo with command history)
3. **Strategy** — PricingEngine (Standard, HappyHour, Loyalty, Weekend)
4. **Observer** — OrderNotifications (Waiter, Manager, Kitchen, AllergyAlert)

### Coherent Pattern Flow
The three required patterns work together in a single flow:
1. **Command** — Waiter places order → KitchenQueue receives PrepareOrderCommand
2. **Strategy** — BillingService applies pricing strategy (HappyHour/Loyalty/etc.)
3. **Singleton** — Confirmed order is written to OrderHistoryLog for analytics

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
```bash
pip install -r requirements.txt
python run.py
```

### Default Login Credentials
| Username | Password | Role |
|----------|----------|------|
| manager | admin123 | Manager |
| chef | chef123 | Head Chef |
| waiter | waiter123 | Waiter |
| cashier | cashier123 | Cashier |

> Passwords are loaded from environment variables (`BITEPLATE_MANAGER_PASSWORD`, etc.) with fallback defaults. See `.env.example` for reference.

### Environment Variables (Optional)
```powershell
# Windows PowerShell
$env:BITEPLATE_MANAGER_PASSWORD="my_secure_password"
$env:BITEPLATE_CHEF_PASSWORD="chef_secret"
python run.py
```

## Project Structure
```
BitePlate/
├── src/
│   ├── config.py          # Configuration (no hardcoded secrets)
│   ├── main.py            # Application entry point
│   ├── models/            # Domain entities
│   │   ├── menu_item.py   # MenuItem + Starter, Main, Dessert, Beverage
│   │   ├── order.py       # Order, OrderItem, OrderStatus
│   │   ├── table.py       # Table, TableStatus
│   │   ├── staff.py       # Staff(ABC) + Manager, HeadChef, Waiter, Cashier
│   │   ├── bill.py        # Bill, BillLineItem
│   │   ├── combo_meal.py  # ComboMeal
│   │   └── reservation.py # Reservation
│   ├── patterns/          # Design patterns
│   │   ├── command.py     # Command, KitchenQueue
│   │   ├── singleton.py   # OrderHistoryLog
│   │   ├── strategy.py    # PricingStrategy + 4 concrete strategies
│   │   └── observer.py    # Subject, Observer + 4 concrete observers
│   ├── services/          # Business logic
│   │   ├── order_service.py
│   │   ├── kitchen_service.py
│   │   ├── billing_service.py
│   │   ├── table_service.py
│   │   └── reservation_service.py
│   ├── ui/                # CustomTkinter GUI
│   │   ├── login_window.py
│   │   ├── main_window.py
│   │   ├── table_view.py
│   │   ├── order_panel.py
│   │   ├── kitchen_display.py
│   │   ├── billing_panel.py
│   │   ├── dashboard.py
│   │   └── components/
│   └── utils/             # Utilities
│       ├── validators.py
│       └── exceptions.py
├── docs/uml/              # PlantUML diagrams
├── tests/                 # Unit tests
├── screenshots/           # Application screenshots
├── README.md
├── EVALUATION.md
└── requirements.txt
```

## Secure Coding Practices
- No hardcoded sensitive values in source code (credentials in `config.py`)
- Input validation via `utils/validators.py`
- Custom exception hierarchy in `utils/exceptions.py`
- Encapsulation enforced via private attributes (`_`) and properties

## Author
- **Name:** [Your Name]
- **Student ID:** [Your ID]
- **Unit:** Unit 27: Advanced Programming (Y/615/1651)
