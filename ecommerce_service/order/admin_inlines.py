from django.contrib import admin
from .models import OrderItem

class OrderItemInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = OrderItem
    extra = 1  # Allows adding new items inline

