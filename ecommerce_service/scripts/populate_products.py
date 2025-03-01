import pymysql
import random
from faker import Faker

# Database Configuration (Update these details)
DB_CONFIG = {
    "host": "<db_name>",
    "user": "<db_user>",
    "password": "<db_pass>",
    "database": "ecommerce",
    "port": 3306  # Change if using a non-default MySQL port
}


# Initialize Faker
fake = Faker()

# Define Categories & Sample Products
PRODUCT_CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker", "Tablet"],
    "Fashion": ["Men’s Jacket", "Women’s Handbag", "Sneakers", "Sunglasses", "T-shirt"],
    "Home Appliances": ["Air Purifier", "Coffee Maker", "Vacuum Cleaner", "Microwave Oven"],
    "Accessories": ["Wristwatch", "Leather Wallet", "Backpack", "Phone Case"]
}

def get_or_create_category(cursor, name, description=""):
    """Ensure the category exists and return its ID."""
    cursor.execute("SELECT id FROM product_category WHERE name = %s", (name,))
    category = cursor.fetchone()

    if category:
        return category[0]  # Return existing category ID

    # Insert new category (id is auto-generated)
    cursor.execute(
        "INSERT INTO product_category (name, description, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())",
        (name, description)
    )
    return cursor.lastrowid  # Get newly inserted category ID

def generate_product(cursor):
    """Generate a single product and return a dictionary with details."""
    category_name = random.choice(list(PRODUCT_CATEGORIES.keys()))
    category_id = get_or_create_category(cursor, category_name)
    product_name = random.choice(PRODUCT_CATEGORIES[category_name])

    return {
        "name": f"{product_name} {fake.random_int(100, 999)}",
        "description": fake.sentence(nb_words=12),
        "category_id": category_id,
        "price": round(random.uniform(10, 5000), 2),  # $10 - $5000
        "stock": random.randint(1, 200)  # Stock between 1 and 200
    }

def create_products(count=10):
    try:
        # Connect to MySQL
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL Query to insert products (id is auto-generated)
        insert_query = """
        INSERT INTO product_product (name, description, category_id, price, stock, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """

        products = []
        for _ in range(count):
            product = generate_product(cursor)
            products.append((
                product["name"],
                product["description"],
                product["category_id"],
                product["price"],
                product["stock"]
            ))

        # Execute batch insert
        cursor.executemany(insert_query, products)
        connection.commit()

        print(f"{count} products added successfully.")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_products(10)  # Change number to insert more/less records
