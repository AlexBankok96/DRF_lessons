from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']

    video_url = serializers.URLField(validators=[validate_video_url])


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.subscriptions.filter(user=user).exists()

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        course = Course.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)
        return course
