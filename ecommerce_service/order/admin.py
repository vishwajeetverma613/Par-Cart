from django.contrib import admin
from .models import Order
from .admin_inlines import OrderItemInline


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__name",)
    inlines = [OrderItemInline]  # Add inline OrderItems within Order admin

