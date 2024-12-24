from celery import shared_task
from django.core.mail import send_mail
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import Subscription
from django.utils.timezone import now, timedelta
@shared_task
def notify_course_update(course_id):
    from .models import Course
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course).select_related('user')

    for subscription in subscribers:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message="Материалы курса обновлены. Проверьте новые уроки!",
            from_email=None,
            recipient_list=[subscription.user.email]
        )

@shared_task
def check_inactive_users():
    from users.models import User
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=one_month_ago)

    for user in inactive_users:
        user.is_active = False
        user.save()


def create_periodic_task():
    schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.DAYS)
    PeriodicTask.objects.create(
        interval=schedule,
        name="Deactivate users who haven't logged in for a month",
        task='courses.tasks.check_inactive_users',
        expires=now() + timedelta(hours=1)
    )