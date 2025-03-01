from django.urls import path
from .views import OrderCreateAPIView, OrderStatusAPIView, OrderMetricsAPIView

urlpatterns = [
    path("orders/", OrderCreateAPIView.as_view(), name="create-order"),
    path("orders/<int:order_id>/", OrderStatusAPIView.as_view(), name="order-status"),
    path("metrics/", OrderMetricsAPIView.as_view(), name="metrics"),
]
