from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PatientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients'

    def ready(self):
        from .signals import create_groups
        post_migrate.connect(create_groups, sender=self)

        from .signals import create_users
        post_migrate.connect(create_users, sender=self)

        from .signals import create_appointments
        post_migrate.connect(create_appointments, sender=self)