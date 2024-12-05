from rest_framework import serializers
from .models import User, Payment

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ['id', 'username', 'email', 'phone', 'city', 'avatar']

class PaymentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Payment
       fields = ['user', 'payment_date', 'paid_course',
                 'paid_lesson',  'amount_paid',
                 'payment_method']