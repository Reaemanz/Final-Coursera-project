# LittleLemonDRF/urls.py

from django.urls import path
from .views import (
    assign_user_to_manager_group,
    ManagerGroupAccessView,
    CategoryListView,
    MenuItemListView,
    assign_user_to_delivery_crew,
    DeliveryCrewOrderListView,
    mark_order_delivered,
    customer_register,
    customer_login
)

urlpatterns = [
    path('assign-user-to-manager-group/<int:user_id>/', assign_user_to_manager_group),
    path('manager-group-access/', ManagerGroupAccessView.as_view(), name='manager-group-access'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('menu-items/', MenuItemListView.as_view(), name='menu-item-list'),
    path('assign-user-to-delivery-crew/<int:user_id>/', assign_user_to_delivery_crew),
    path('delivery-crew-orders/', DeliveryCrewOrderListView.as_view(), name='delivery-crew-order-list'),
    path('mark-order-delivered/<int:order_id>/', mark_order_delivered),
    path('customer-register/', customer_register, name='customer-register'),
    path('customer-login/', customer_login, name='customer-login'),
]
