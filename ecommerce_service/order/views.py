from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, OrderItem
from product.models import Product
from customer.models import Customer
from order.serializers import OrderCreateSerializer, OrderSerializer
from order.tasks import process_order_task
from django.db.models import Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from common.enums import OrderStatus
from django.db.models import Avg, F, ExpressionWrapper, DurationField


class OrderCreateAPIView(APIView):
    """
    API to create an order.
    """

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer_id = serializer.validated_data["customer_id"]
        items = serializer.validated_data["items"]

        try:
            with transaction.atomic():
                customer = Customer.objects.get(id=customer_id)
                order = Order.objects.create(customer=customer, total_amount=0, status=OrderStatus.PENDING.value)
                total_price = 0
                order_items = []

                for item in items:
                    product = Product.objects.select_for_update().get(id=item["product_id"])

                    

                    price = product.price * item["quantity"]
                    order_items.append(OrderItem(order=order, product=product, quantity=item["quantity"], price=price))

                    product.save()

                    total_price += price

                OrderItem.objects.bulk_create(order_items)
                order.total_amount = total_price
                order.save()

                # Push order to Celery queue
                process_order_task.delay(order.id)

                return Response({"order_id": order.id, "status": order.status}, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OrderStatusAPIView(APIView):
    """
    API to fetch order details and current status.
    """

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderMetricsAPIView(APIView):
    """
    API to fetch key metrics:
    - Total orders processed
    - Average processing time
    - Order count per status
    """

    def get(self, request):
        total_orders = Order.objects.count()
        avg_processing_time = Order.objects.filter(status=OrderStatus.COMPLETED).annotate(
            processing_duration=ExpressionWrapper(F('processed_at') - F('created_at'), output_field=DurationField())
        ).aggregate(avg_duration=Avg('processing_duration'))['avg_duration']
        order_status_counts = Order.objects.values('status').annotate(count=Count('status'))
        status_count_dict = {status['status']: status['count'] for status in order_status_counts}

        return Response({
            "total_orders": total_orders,
            "orders_by_status": status_count_dict,
            "avg_processing_time": avg_processing_time
        }, status=status.HTTP_200_OK)