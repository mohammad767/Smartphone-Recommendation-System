from django.apps import AppConfig


class SmartphonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.smartphones"
    
    def ready(self):
        import apps.smartphones.signals