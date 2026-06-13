# BitePlate Web - Smart Restaurant Management System

## Overview
BitePlate Web is a modern restaurant management system built using Django, Object-Oriented Programming principles, and industry-recognized design patterns. It replaces paper-based and legacy processes with a maintainable, scalable web-based solution.

## Language & IDE Justification
- **Language:** Python 3.10+ — Chosen for its readability, extensive standard library, and strong OOP support.
- **IDE:** VS Code — Lightweight, excellent Python support, integrated terminal, and Git integration.
- **Web Framework:** Django 5.0+ — Robust, secure, and scalable web framework with built-in ORM, admin panel, and templating.

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
# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start the development server
python run.py
# or
python manage.py runserver
```

### Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

### Default Login Credentials
| Username | Password | Role |
|----------|----------|------|
| manager | admin123 | Manager |
| chef | chef123 | Head Chef |
| waiter | waiter123 | Waiter |
| cashier | cashier123 | Cashier |

> Passwords are loaded from environment variables (`BITEPLATE_MANAGER_PASSWORD`, etc.) with fallback defaults.

## Project Structure
```
BitePlateWeb/
├── biteplate_web/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Django app (web views, ORM models)
│   ├── models.py        # Django ORM models
│   ├── views.py         # Web views/routes
│   └── urls.py
├── src/                 # OOP Pattern Implementation (100% same as desktop version)
│   ├── models/          # Domain entities (MenuItem, Order, Table, Staff, Bill, etc.)
│   ├── patterns/        # Design patterns (Singleton, Command, Strategy, Observer)
│   ├── services/        # Business logic (OrderService, KitchenService, etc.)
│   ├── utils/           # Validators and exceptions
│   └── config.py        # Configuration
├── templates/           # HTML templates
├── static/css/          # CSS styles
├── docs/uml/            # PlantUML diagrams
├── manage.py
├── run.py
├── README.md
├── EVALUATION.md
└── requirements.txt
```

## UML Diagrams
All UML diagrams are located in `docs/uml/`:
- `core_system.puml` — Core System Class Diagram
- `use_case_diagram.puml` — Use Case Diagram
- `sequence_strategy.puml` — Strategy Pattern Sequence
- `sequence_observer.puml` — Observer Pattern Sequence
- `sequence_command.puml` — Command Pattern Sequence

## Secure Coding Practices
- No hardcoded sensitive values in source code (credentials in `config.py`)
- Input validation via `utils/validators.py`
- Custom exception hierarchy in `utils/exceptions.py`
- Encapsulation enforced via private attributes (`_`) and properties

## Author
- **Unit:** Unit 27: Advanced Programming (Y/615/1651)
- **Assignment:** BitePlate Smart Restaurant Management System
