from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from courses.models import Course, Lesson

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
    )

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
