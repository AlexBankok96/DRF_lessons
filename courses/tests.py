from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription
from rest_framework import status

class CourseAPITests(APITestCase):
    def setUp(self):

        get_user_model().objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Subscription.objects.all().delete()

        self.user = get_user_model().objects.create_user(username='user', password='pass')
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, video_url="https://youtube.com")

    def test_course_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/courses/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Subscription added")

    def test_course_unsubscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/courses/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Subscription added")

        response = self.client.post('/api/v1/courses/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Subscription removed")

    def test_lesson_list_pagination(self):
        for i in range(15):
            Lesson.objects.create(
                title=f"Lesson {i}",
                course=self.course,
                video_url="https://youtube.com"
            )


        print("Количество уроков в базе:", Lesson.objects.count())

        self.client.force_authenticate(user=self.user)


        response = self.client.get(f'/api/v1/lessons/?course_id={self.course.id}')
        print("Данные первой страницы:", response.data['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)

        next_url = response.data['next']
        response = self.client.get(next_url)
        print("Данные второй страницы:", response.data['results'])
        self.assertEqual(len(response.data['results']), 5)
