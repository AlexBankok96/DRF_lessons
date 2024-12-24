from django.urls import path
from .views import UserListView, UserDetailView, PaymentListView, PaymentCreateAPIView



urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),

    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/v1/payments/', PaymentListView.as_view(), name='payment-list'),
    path('api/v1/payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]
