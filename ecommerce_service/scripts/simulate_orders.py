import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# API URL
ORDER_API_URL = "http://127.0.0.1:5598/api/v1/orders/"  # Replace with actual API URL

# Number of orders to create
NUM_ORDERS = 1000
MAX_ITEMS_PER_ORDER = 5

# Sample customer and product IDs (Replace with real IDs from your DB)
CUSTOMER_IDS = [857125, 857126, 857127, 857128, 857129]  # Replace with real customer IDs
PRODUCT_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Replace with real product IDs


def create_order():
    """Sends a request to create an order with the correct request body format."""
    customer_id = random.choice(CUSTOMER_IDS)
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    items = [{"product_id": random.choice(PRODUCT_IDS), "quantity": random.randint(1, 3)} for _ in range(num_items)]

    payload = {
        "customer_id": customer_id,
        "items": items
    }

    try:
        response = requests.post(ORDER_API_URL, json=payload)
        if response.status_code == 201:
            print(f"✅ Order created successfully: {response.json().get('id')}")
        else:
            print(f"❌ Failed to create order: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")


def simulate_orders():
    """Simulates concurrent order creation by making API calls."""
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:  # 20 concurrent workers
        executor.map(lambda _: create_order(), range(NUM_ORDERS))

    print(f"✅ {NUM_ORDERS} orders simulated in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    simulate_orders()
