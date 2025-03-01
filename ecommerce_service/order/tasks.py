from celery import shared_task
import time
from django.db import transaction
from order.models import Order
from common.enums import OrderStatus
from django.utils.timezone import now
import random


@shared_task
def process_order_task(order_id):
    """
    Process the order asynchronously.
    """
    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)

            if order.status != OrderStatus.PENDING.value:
                return

            order.status = OrderStatus.PROCESSING.value
            order.save()

            # Simulating random order processing time (between 3 to 10 seconds)
            sleep_time = random.uniform(3, 10)
            time.sleep(sleep_time)

            order.status = OrderStatus.COMPLETED.value
            order.processed_at = now()
            order.save()

            print(f"Order {order_id} placed successfully in {sleep_time:.2f} seconds")


    except Exception as e:
        print(f"Error processing order {order_id}: {str(e)}")

