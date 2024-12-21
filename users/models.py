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

class Payments(models.Model):
    payment_choices = [
        ('Cash', "наличные"),
        ('Transfer', "перевод"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='user'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Оплаченный курс',
        blank=True,
        null=True,
        related_name='payments'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Оплаченный урок',
        blank=True,
        null=True,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    payment_type = models.CharField(
        max_length=50,
        choices=payment_choices,
        verbose_name='тип оплаты'
    )

    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='pending')
    payment_url = models.URLField(max_length=450, verbose_name="Ссылка на оплату", null=True, blank=True)
    session_id = models.CharField(max_length=255, verbose_name="ID сессии", null=True, blank=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-date']

    def __str__(self):
        return f'Пользователь {self.user} оплатил {self.amount}'