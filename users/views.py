from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from .permissions import IsModerator

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['paid_course__title', 'paid_lesson__title', 'payment_method']
