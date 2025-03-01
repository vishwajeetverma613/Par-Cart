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
import logging
import json
from scripts.simulate_orders import simulate_orders
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



console_logger = logging.getLogger('console')


@method_decorator(csrf_exempt, name="dispatch")
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
                    product = Product.objects.get(id=item["product_id"])

                    

                    price = product.price * item["quantity"]
                    order_items.append(OrderItem(order=order, product=product, quantity=item["quantity"], price=price))

                    total_price += price

                OrderItem.objects.bulk_create(order_items)
                order.total_amount = total_price
                order.save()

                # Push order to Celery queue
                console_logger.info({"message": f"sucessfully Created Order with order ID => {order.id}"})
                process_order_task.delay(order.id)

                return Response({"order_id": order.id, "status": order.status}, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            console_logger.error({"message":  "Invalid customer ID", "meta": {"request": json.dumps(request.data)}})
            return Response({"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            console_logger.error({"message":  "Invalid product ID", "meta": {"request": json.dumps(request.data)}})
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            traceback.print_exc()
            console_logger.error({"message":  f"An error Occurred {str(e)} => {e.__traceback__}", "meta": {"request": json.dumps(request.data)}})
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
            console_logger.info({"message": f"Order with order ID => {order_id} not Found"})
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
        avg_processing_time = Order.objects.filter(status=OrderStatus.COMPLETED.value).annotate(
            processing_duration=ExpressionWrapper(F('processed_at') - F('created_at'), output_field=DurationField())
        ).aggregate(avg_duration=Avg('processing_duration'))['avg_duration']
        order_status_counts = Order.objects.values('status').annotate(count=Count('status'))
        status_count_dict = {status['status']: status['count'] for status in order_status_counts}

        return Response({
            "total_orders": total_orders,
            "orders_by_status": status_count_dict,
            "avg_processing_time": avg_processing_time.total_seconds()
        }, status=status.HTTP_200_OK)
    


# views.py
from django.http import JsonResponse

@csrf_exempt
def run_script_view(request):
    if request.method == 'POST':
        # Your Python logic here
        import threading
        threading.Thread(target=simulate_orders).start()
        result = "Load Simulation started. Please go to Rabbitmq portal to see the load."
        return JsonResponse({'result': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)
