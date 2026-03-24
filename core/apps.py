from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        from django.contrib.auth.models import Group

        from core.auth import ALL_ROLES
        import core.signals  # noqa

        @receiver(post_migrate, sender=self)
        def ensure_groups(sender, **kwargs):
            for g in ALL_ROLES:
                Group.objects.get_or_create(name=g)
