from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson


class CourseAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user', password='pass')
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, video_url="https://youtube.com")

    def test_course_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/courses/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Subscription added")
