from celery import shared_task
import time
from django.db import transaction
from order.models import Order
from common.enums import OrderStatus
from django.utils.timezone import now
import random
import logging
import json

console_logger = logging.getLogger('console')



@shared_task
def process_order_task(order_id):
    """
    Process the order asynchronously.
    """
    try:
        with transaction.atomic():
            console_logger.info({"messge": f"Recieved Task for processing Order with order ID => {order_id}"})
            order = Order.objects.select_for_update().get(id=order_id)

            if order.status != OrderStatus.PENDING.value:
                return

            order.status = OrderStatus.PROCESSING.value
            order.save()

            # Simulating random order processing time (between 3 to 5 seconds)
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)

            order.status = OrderStatus.COMPLETED.value
            order.processed_at = now()
            order.save()

            print(f"Order {order_id} placed successfully in {sleep_time:.2f} seconds")
            console_logger.info({"messge": f"Order {order_id} placed successfully in {sleep_time:.2f} seconds"})


    except Exception as e:
        print(f"Error processing order {order_id}: {str(e)}")
        console_logger.info({"messge": f"Error processing order {order_id}: {str(e)}"})


