from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'


class CoursesConfig(AppConfig):
    name = 'courses'

    def ready(self):
        from .tasks import create_periodic_task
        create_periodic_task()