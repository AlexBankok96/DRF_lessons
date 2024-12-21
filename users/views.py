from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from .models import User, Payments
from .serializers import UserSerializer, PaymentSerializer
from .services import create_stripe_session, create_stripe_product, create_stripe_price


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['paid_course__title', 'paid_lesson__title', 'payment_method']


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        price = create_stripe_price(
            stripe_product_id=stripe_product_id, amount=payment.amount
        )
        session_id, payment_link = create_stripe_session(price=price)
        payment.stripe_session_id = session_id
        payment.payment_url = payment_link
        payment.save()
