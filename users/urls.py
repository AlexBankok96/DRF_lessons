from django.urls import path
from .views import UserListView, UserDetailView, PaymentListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]