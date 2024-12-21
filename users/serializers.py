from rest_framework import serializers
from .models import User, Payments

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ['id', 'username', 'email', 'phone', 'city', 'avatar']

class PaymentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Payments
       fields = ['user', 'date', 'paid_course', 'paid_lesson', 'amount', 'payment_type']