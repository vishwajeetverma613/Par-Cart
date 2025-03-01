import pymysql
import random
from faker import Faker

# Database Configuration (Update these details)


DB_CONFIG = {
    "host": "database-1.cluster-cngmgcuearcw.ap-south-1.rds.amazonaws.com",
    "user": "admin",
    "password": "vynzoEAG6Cl7Qawoh8vW",
    "database": "ecommerce",
    "port": 3306  # Change if using a non-default MySQL port
}

# Initialize Faker
fake = Faker()

def create_customers(count=10):
    try:
        # Connect to MySQL
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL Query to insert data
        insert_query = """
        INSERT INTO customer_customer (name, email, phone, created_at, updated_at, is_active)
        VALUES ( %s, %s, %s, NOW(), NOW(), 1)
        """

        customers = []
        for _ in range(count):
            customers.append((
                fake.name(),
                fake.unique.email(),
                fake.phone_number()[:15]  # Ensuring max_length is 15
            ))

        # Execute batch insert
        cursor.executemany(insert_query, customers)
        connection.commit()

        print(f"{count} customers added successfully.")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_customers(10)  # Change number to insert more/less records
