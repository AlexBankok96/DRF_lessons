from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from django.shortcuts import redirect

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('', lambda request: redirect('/api/v1/')),
    path('api/v1/', include('users.urls')),

    path('api/v1/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('api/v1/lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-retrieve'),
    path('api/v1/lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('api/v1/lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-destroy'),
]
