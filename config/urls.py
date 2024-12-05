from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, LessonListCreateView, LessonRetrieveView
from users.views import UserListView, UserDetailView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(router.urls)),
   path('api/v1/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
   path('api/v1/lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-retrieve'),
   path('api/v1/users/', UserListView.as_view(), name='user-list'),
   path('api/v1/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]