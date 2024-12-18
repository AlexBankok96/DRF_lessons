from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель курса",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'course')
