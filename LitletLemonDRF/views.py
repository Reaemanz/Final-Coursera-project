from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from .models import CustomUser, Category, MenuItem, Order, OrderItem, UserProfile
from rest_framework.authtoken.models import Token
from djoser.views import TokenCreateView
from .serializers import (
    UserSerializer, CategorySerializer, MenuItemSerializer,
    OrderSerializer, OrderItemSerializer, UserProfileSerializer
)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def assign_user_to_manager_group(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    manager_group = Group.objects.get(name='manager')
    user.groups.add(manager_group)
    return Response({'message': f'User {user.username} assigned to manager group successfully.'}, status=status.HTTP_200_OK)

class ManagerGroupAccessView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(groups__name='manager')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAdminUser]

# Other views for managers, delivery crew, and customers can be implemented similarly

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def assign_user_to_delivery_crew(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    delivery_crew_group = Group.objects.get(name='delivery_crew')
    user.groups.add(delivery_crew_group)
    return Response({'message': f'User {user.username} assigned to delivery crew successfully.'}, status=status.HTTP_200_OK)

class DeliveryCrewOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsInDeliveryCrew]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(delivery_crew=user.profile)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated, permissions.IsInDeliveryCrew])
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, delivery_crew=request.user.profile)
    order.status = 'Delivered'
    order.save()
    return Response({'message': f'Order {order_id} marked as delivered successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def customer_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Customer registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer