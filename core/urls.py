from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tables/', views.tables_view, name='tables'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('billing/', views.billing_view, name='billing'),
    path('history/', views.history_view, name='history'),
    path('reservations/', views.reservations_view, name='reservations'),
    path('staff/', views.staff_view, name='staff'),
    path('alerts/', views.alerts_view, name='alerts'),
]
