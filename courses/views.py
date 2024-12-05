from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
   queryset = Course.objects.all()
   serializer_class = CourseSerializer
   filter_backends = [SearchFilter, OrderingFilter]
   search_fields = ['title', 'description']

class LessonListCreateView(generics.ListCreateAPIView):
   queryset = Lesson.objects.all()
   serializer_class = LessonSerializer
   filter_backends = [SearchFilter]
   search_fields = ['title']

class LessonRetrieveView(generics.RetrieveAPIView):
   queryset = Lesson.objects.all()
   serializer_class = LessonSerializer

class LessonUpdateView(generics.UpdateAPIView):
   queryset = Lesson.objects.all()
   serializer_class = LessonSerializer

class LessonDestroyView(generics.DestroyAPIView):
   queryset = Lesson.objects.all()
   serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Lesson.objects.all()
   serializer_class = LessonSerializer