from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Table(models.Model):
    STATUS_CHOICES = [
        ('free', 'Free'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('awaiting_bill', 'Awaiting Bill'),
        ('cleared', 'Cleared'),
    ]
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free')

    def __str__(self):
        return f"Table {self.number} ({self.status})"

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

    @property
    def total(self):
        return self.menu_item.price * self.quantity

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests_count = models.IntegerField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation - {self.guest_name} ({self.date} {self.time})"

class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bills')
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, blank=True, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
    ])

    def __str__(self):
        return f"Bill #{self.id} - ${self.total}"

    def calculate_totals(self):
        self.subtotal = sum(item.total for item in self.order.items.all())
        self.tax = self.subtotal * 0.10
        self.total = self.subtotal + self.tax + self.tip - self.discount
        self.save()
