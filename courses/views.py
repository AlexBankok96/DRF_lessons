from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if not course_id:
            raise KeyError('course_id не найден в параметрах запроса.')

        return Lesson.objects.filter(course_id=course_id).order_by('id')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class SubscriptionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)

        if not created:
            subscription.delete()
            return Response({"message": "Subscription removed"}, status=status.HTTP_200_OK)

        return Response({"message": "Subscription added"}, status=status.HTTP_201_CREATED)
