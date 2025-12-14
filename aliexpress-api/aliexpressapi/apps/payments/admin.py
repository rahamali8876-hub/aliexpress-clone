from django.contrib import admin
from apps.payments.models.payment import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "provider",
        "amount",
        "status",
        "created_at",
    )

    list_filter = ("provider", "status", "created_at")
    readonly_fields = (
        "id",
        "order",
        "provider",
        "amount",
        "status",
        "gateway_reference",
        "idempotency_key",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
