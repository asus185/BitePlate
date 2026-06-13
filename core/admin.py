from django.contrib import admin
from .models import Table, MenuItem, Order, OrderItem, Reservation, Bill

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'status')
    list_filter = ('status',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available')
    list_filter = ('category', 'available')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'table', 'date', 'time', 'confirmed')
    list_filter = ('confirmed',)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'total', 'paid', 'payment_method')
    list_filter = ('paid', 'payment_method')
