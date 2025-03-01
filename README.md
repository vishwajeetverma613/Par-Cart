# E-Commerce Backend API

## Overview

This project is a **Django-based e-commerce backend system** that provides order management, and an admin panel. It is hosted on **AWS** and containerized using **Docker**.

## Features

- **Order Processing**: Create and manage customer orders.
- **Admin Panel**: Manage orders, products, and users.
- **Logging & Monitoring**: Integrated with **ELK Stack (Elasticsearch, Logstash, Kibana)**.
- **Asynchronous Processing**: Uses **RabbitMQ with Celery** for background tasks.
- **API Documentation**: Available via **Swagger**.

---

## **Tech Stack**

### **Backend**

- Django (Django Rest Framework)
- MySQL (Relational Database)
- RabbitMQ (Message Broker)

### **Logging & Monitoring**

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Filebeat** (Log Forwarding)

### **Deployment & Infrastructure**

- **AWS** (EC2, RDS)
- **Docker & Docker Compose**

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/ecommerce-backend.git
cd ecommerce-backend
```

### **2. Environment Configuration**

Create a `.env` file and configure the necessary environment variables:

```
DATABASE_URL=mysql://username:password@db_host:3306/db_name
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://rabbitmq:5672/
ELASTICSEARCH_URL=http://elasticsearch:9200
```

### **3. Docker Setup**

Run the following command to start the services:

```bash
docker-compose up -d --build -d
docker-compose -f docker-compose-queue.yml up -d --build -d

```

### **4. Run Database Migrations**

```bash
DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py migrate
```

### **5. Create a Superuser for Admin Panel**

```bash
DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py createsuperuser
```

### **6. Access the Application**

- **API Server**: [http://13.201.1.102:8000/api/v1/]
- **Admin Panel**: [http://13.201.1.102:8000/admin/] (username: guest, password: fuVUhqMt9t5j2ev)
- **Swagger UI**: [http://13.201.1.102:8000/swagger/]
- **RabbitMQ Admin Panel**: [http://13.201.1.102:15672/](username: guest_viewer, password: user_paskjnknks)
- **Kibana Dashboard**: [http://13.201.1.102:5601/]
---

## **Logging & Monitoring Setup**

### **1. ELK Stack Setup**

- Install **Elasticsearch**, **Logstash**, and **Kibana** via Docker Compose.

```bash
docker-compose -f elk-stack-compose.yml up -d
```

- Configure **Logstash** to collect logs from Django.
- Use **Filebeat** to forward logs to **Elasticsearch**.

### **2. Filebeat Configuration**

Create a `filebeat.yml` file:

```yml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/django/*.log
output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```


## **API Endpoints**

| Method | Endpoint               | Description            |
| ------ | ---------------------- | ---------------------- |
| GET    | `/api/v1/metrics/`     | Retrieve order metrics |
| POST   | `/api/v1/orders/`      | Create a new order     |
| GET    | `/api/v1/orders/{id}/` | Retrieve order details |

---

## **Swagger Documentation**

To access Swagger UI, visit:

```bash
http://127.0.0.1:8000/swagger/
```

If using a **YAML file**, place it in `static/swagger/swagger.yaml`.

---
