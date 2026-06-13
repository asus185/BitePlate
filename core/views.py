from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps
from datetime import datetime

# Import OOP services and patterns
from config import DEFAULT_STAFF
from models.staff import Manager, HeadChef, Waiter, Cashier, Role
from services.table_service import TableService
from services.order_service import OrderService
from services.kitchen_service import KitchenService
from services.billing_service import BillingService
from services.reservation_service import ReservationService
from patterns.strategy import StandardPricing, HappyHourPricing, LoyaltyCardPricing, WeekendSurchargePricing
from patterns.singleton import OrderHistoryLog
from patterns.observer import WaiterNotifier, ManagerDashboard, KitchenDisplay, AllergyAlert

# Global services instance
table_service = TableService()
order_service = OrderService()
kitchen_service = KitchenService()
billing_service = BillingService()
reservation_service = ReservationService()

# Sample menu items
SAMPLE_MENU = [
    {"id": "S001", "name": "Bruschetta", "price": 8.99, "category": "starter", "type": "Starter"},
    {"id": "S002", "name": "Soup of the Day", "price": 6.99, "category": "starter", "type": "Starter"},
    {"id": "M001", "name": "Grilled Steak", "price": 24.99, "category": "main", "type": "MainCourse"},
    {"id": "M002", "name": "Chicken Parmesan", "price": 18.99, "category": "main", "type": "MainCourse"},
    {"id": "M003", "name": "Pasta Carbonara", "price": 16.99, "category": "main", "type": "MainCourse"},
    {"id": "D001", "name": "Tiramisu", "price": 7.99, "category": "dessert", "type": "Dessert"},
    {"id": "D002", "name": "Chocolate Cake", "price": 6.99, "category": "dessert", "type": "Dessert"},
    {"id": "B001", "name": "Soft Drink", "price": 2.99, "category": "beverage", "type": "Beverage", "size": "Medium"},
    {"id": "B002", "name": "Wine Glass", "price": 9.99, "category": "beverage", "type": "Beverage", "size": "Medium", "alcoholic": True},
]

def get_staff_user(username, password):
    """Authenticate staff user"""
    user_data = DEFAULT_STAFF.get(username)
    if user_data and user_data["password"] == password:
        role_map = {"manager": Manager, "chef": HeadChef, "waiter": Waiter, "cashier": Cashier}
        role_class = role_map[user_data["role"]]
        return role_class(
            staff_id=user_data["staff_id"],
            username=user_data["username"],
            password=user_data["password"],
            name=user_data["name"]
        )
    return None

def check_perm(user, permission):
    """Permission tekshirish helper"""
    if not user:
        return False
    return user.get('permissions', {}).get(permission, False)

def session_required(view_func):
    """Custom session decorator - Django auth o'rniga session tekshiradi"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.session.get('user')
        if not user:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_view(request):
    """Login sahifasi"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = get_staff_user(username, password)
        if user:
            request.session['user'] = {
                'staff_id': user.staff_id,
                'username': user.username,
                'name': user.name,
                'role': user.role.value,
                'permissions': user.permissions,
            }
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    """Logout"""
    request.session.flush()
    return redirect('login')

@session_required
def dashboard_view(request):
    """Dashboard - role-based"""
    user = request.session.get('user')

    tables = table_service.get_all_tables()
    orders = order_service.get_all_orders()

    perms = user.get('permissions', {})
    context = {
        'user': user,
        'tables': tables,
        'orders': orders,
        'table_count': len(tables),
        'order_count': len(orders),
        'perms': perms,
    }
    return render(request, 'dashboard.html', context)

@session_required
def tables_view(request):
    """Tables management"""
    user = request.session.get('user')
    tables = table_service.get_all_tables()

    if request.method == 'POST':
        action = request.POST.get('action')
        table_number = int(request.POST.get('table_number'))

        if action == 'occupy':
            order = order_service.create_order(table_number, user['staff_id'])
            table_service.occupy_table(table_number, order.order_id)
        elif action == 'reserve':
            table_service.reserve_table(table_number, f"RES-{table_number}")
        elif action == 'await_bill':
            table_service.await_bill(table_number)
        elif action == 'clear':
            table_service.clear_table(table_number)
        elif action == 'free':
            table_service.free_table(table_number)

        return redirect('tables')

    return render(request, 'tables.html', {
        'tables': tables,
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def orders_view(request):
    """Orders management"""
    user = request.session.get('user')
    orders = order_service.get_all_orders()
    menu_items = SAMPLE_MENU

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            table_number = int(request.POST.get('table_number'))
            order = order_service.create_order(table_number, user['staff_id'])
            return redirect('order_detail', order_id=order.order_id)
        elif action == 'confirm':
            order_id = request.POST.get('order_id')
            order_service.confirm_order(order_id)
            kitchen_service.add_order_to_queue(order_service.get_order(order_id))
        elif action == 'cancel':
            order_id = request.POST.get('order_id')
            order = order_service.get_order(order_id)
            if order and order.can_modify():
                from models.order import OrderStatus
                order.status = OrderStatus.CANCELLED
                messages.success(request, f'Order {order_id} cancelled')

    return render(request, 'orders.html', {
        'orders': orders,
        'menu_items': menu_items,
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def order_detail_view(request, order_id):
    """Order detail - add items"""
    order = order_service.get_order(order_id)
    if not order:
        return redirect('orders')

    menu_items = SAMPLE_MENU

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_item':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            menu_item_data = next((m for m in menu_items if m['id'] == item_id), None)
            if menu_item_data:
                from models.menu_item import MainCourse, Starter, Dessert, Beverage
                type_map = {
                    'Starter': Starter,
                    'MainCourse': MainCourse,
                    'Dessert': Dessert,
                    'Beverage': Beverage,
                }
                cls = type_map.get(menu_item_data['type'], MainCourse)
                menu_item = cls(
                    item_id=menu_item_data['id'],
                    name=menu_item_data['name'],
                    base_price=menu_item_data['price'],
                )
                order_service.add_item_to_order(order_id, menu_item, quantity)

        elif action == 'remove_item':
            item_index = int(request.POST.get('item_index', 0))
            order.remove_item(item_index)
            messages.success(request, 'Item removed from order')

        elif action == 'confirm':
            order_service.confirm_order(order_id)
            kitchen_service.add_order_to_queue(order)
            return redirect('orders')

        elif action == 'create_bill':
            bill = billing_service.create_bill(order)
            return redirect('billing')

    return render(request, 'order_detail.html', {
        'order': order,
        'menu_items': menu_items,
        'user': request.session.get('user'),
        'perms': request.session.get('user', {}).get('permissions', {}),
    })

@session_required
def kitchen_view(request):
    """Kitchen queue management"""
    user = request.session.get('user')
    queue = kitchen_service.queue

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'process_next':
            queue.execute_next()
        elif action == 'undo_last':
            queue.undo_last()
        elif action == 'process_all':
            queue.execute_all()

    return render(request, 'kitchen.html', {
        'queue_status': queue.get_queue_status(),
        'queue': queue.queue,
        'history': queue.history,
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def billing_view(request):
    """Billing and POS"""
    user = request.session.get('user')
    bills = billing_service.get_all_bills()

    if request.method == 'POST':
        action = request.POST.get('action')
        bill_id = request.POST.get('bill_id')

        if action == 'create':
            order_id = request.POST.get('order_id')
            order = order_service.get_order(order_id)
            if order:
                bill = billing_service.create_bill(order)

        elif action == 'apply_strategy':
            strategy = request.POST.get('strategy')
            strategy_map = {
                'standard': StandardPricing(),
                'happyhour': HappyHourPricing(),
                'loyalty': LoyaltyCardPricing(),
                'weekend': WeekendSurchargePricing(),
            }
            billing_service.pricing_engine.strategy = strategy_map.get(strategy, StandardPricing())
            billing_service.calculate_total(bill_id)

        elif action == 'set_tip':
            tip = float(request.POST.get('tip', 0))
            billing_service.set_tip(bill_id, tip)

        elif action == 'close':
            method = request.POST.get('payment_method', 'cash')
            billing_service.close_bill(bill_id, method)

        elif action == 'split':
            people = int(request.POST.get('people', 2))
            split_amount = billing_service.split_bill(bill_id, people)
            messages.info(request, f"Split bill: ${split_amount:.2f} per person")

        elif action == 'view_receipt':
            receipt = billing_service.generate_receipt(bill_id)
            if receipt:
                return render(request, 'receipt.html', {
                    'receipt': receipt,
                    'bill_id': bill_id,
                    'user': user,
                    'perms': user.get('permissions', {}),
                })

        return redirect('billing')

    return render(request, 'billing.html', {
        'bills': bills,
        'orders': order_service.get_all_orders(),
        'current_strategy': billing_service.pricing_engine.get_current_strategy_name(),
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def history_view(request):
    """Order history (Singleton)"""
    user = request.session.get('user')
    history_log = OrderHistoryLog()

    all_orders = history_log.get_all_orders()
    total_revenue = history_log.get_total_revenue()
    peak_hours = history_log.get_peak_hours()
    most_frequent = history_log.get_most_frequent_item()

    return render(request, 'history.html', {
        'orders': all_orders,
        'total_revenue': total_revenue,
        'peak_hours': peak_hours,
        'most_frequent': most_frequent,
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def reservations_view(request):
    """Reservations management"""
    user = request.session.get('user')
    reservations = reservation_service.get_all_reservations()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            customer_name = request.POST.get('customer_name')
            phone = request.POST.get('phone')
            table_number = int(request.POST.get('table_number'))
            date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
            party_size = int(request.POST.get('party_size'))
            special_requests = request.POST.get('special_requests', '')

            reservation_service.create_reservation(
                customer_name, phone, table_number, date, party_size, special_requests
            )

        elif action == 'confirm':
            res_id = request.POST.get('reservation_id')
            reservation_service.confirm_reservation(res_id)

        elif action == 'cancel':
            res_id = request.POST.get('reservation_id')
            reservation_service.cancel_reservation(res_id)

    return render(request, 'reservations.html', {
        'reservations': reservations,
        'tables': table_service.get_all_tables(),
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def staff_view(request):
    """Manager - Staff boshqaruvi (UC16)"""
    user = request.session.get('user')
    if not check_perm(user, 'manage_staff'):
        messages.error(request, 'Permission denied')
        return redirect('dashboard')

    staff_list = [
        {"staff_id": "M001", "name": "John Manager", "role": "Manager", "username": "manager"},
        {"staff_id": "C001", "name": "Chef Gordon", "role": "Head Chef", "username": "chef"},
        {"staff_id": "W001", "name": "Waiter Sarah", "role": "Waiter", "username": "waiter"},
        {"staff_id": "CA001", "name": "Cashier Mike", "role": "Cashier", "username": "cashier"},
    ]

    return render(request, 'staff.html', {
        'staff_list': staff_list,
        'user': user,
        'perms': user.get('permissions', {}),
    })

@session_required
def alerts_view(request):
    """Receive Alerts - Observer Pattern (UC17)"""
    user = request.session.get('user')

    all_orders = order_service.get_all_orders()

    waiter_notifications = []
    manager_alerts = []
    kitchen_orders = []
    allergy_alerts_list = []

    if all_orders:
        for order in all_orders:
            subject = order_service._order_subjects.get(order.order_id)
            if subject:
                wn = WaiterNotifier(user['staff_id'])
                md = ManagerDashboard()
                kd = KitchenDisplay()
                aa = AllergyAlert()

                subject.attach(wn)
                subject.attach(md)
                subject.attach(kd)
                subject.attach(aa)

                subject.notify()

                waiter_notifications.extend(wn.get_notifications())
                manager_alerts.extend(md.get_alerts())
                kitchen_orders.extend(kd.get_orders())
                allergy_alerts_list.extend(aa.get_alerts())
    else:
        from models.order import Order, OrderStatus
        from patterns.observer import OrderSubject
        from models.menu_item import MainCourse

        demo_order = Order("DEMO-001", 1, user['staff_id'])
        demo_item = MainCourse("M001", "Grilled Steak", 24.99)
        demo_item.add_allergen("Gluten")
        demo_item.add_allergen("Dairy")
        demo_order.add_item(demo_item, 2)

        subject = OrderSubject(demo_order)
        wn = WaiterNotifier(user['staff_id'])
        md = ManagerDashboard()
        kd = KitchenDisplay()
        aa = AllergyAlert()

        subject.attach(wn)
        subject.attach(md)
        subject.attach(kd)
        subject.attach(aa)

        subject.set_status(OrderStatus.CONFIRMED)
        subject.set_status(OrderStatus.PREPARING)

        waiter_notifications = wn.get_notifications()
        manager_alerts = md.get_alerts()
        kitchen_orders = kd.get_orders()
        allergy_alerts_list = aa.get_alerts()

    alerts = {
        'waiter': waiter_notifications,
        'manager': manager_alerts,
        'kitchen': kitchen_orders,
        'allergy': allergy_alerts_list,
    }

    return render(request, 'alerts.html', {
        'alerts': alerts,
        'user': user,
        'perms': user.get('permissions', {}),
    })
