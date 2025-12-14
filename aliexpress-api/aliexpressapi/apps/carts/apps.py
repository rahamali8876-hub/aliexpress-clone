from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.carts"

    def ready(self):
        import apps.carts.signals


# from django.apps import AppConfig


# class CartsConfig(AppConfig):
#     name = "apps.carts"

#     def ready(self):
#         import apps.carts.signals
