# E-Commerce Backend System

## 🚀 Overview
This **E-Commerce Backend System** is a **high-performance, scalable, and modular** solution tailored for **order management, real-time monitoring, and seamless integrations**. Built using **Django** and **Django Rest Framework (DRF)**, this backend is designed to be robust, efficient, and easily extendable.

🔹 **Key Highlights:**
- **Microservices-Oriented Architecture** for better modularity and scalability.
- **Advanced Logging & Monitoring** with **ELK Stack**.
- **Asynchronous Processing** powered by **RabbitMQ and Celery**.
- **Containerized Deployment** using **Docker & Docker Compose**.
- **Cloud-Native Infrastructure** hosted on **AWS**.

---

## 🏗️ System Architecture

### **1️⃣ Microservices-Oriented Design**
The backend is structured into distinct Django apps, ensuring modularity and ease of expansion:

- **🛒 Orders** → Manages order creation, updates, and real-time tracking.
- **📦 Products** → Handles product catalog, inventory, and pricing management.
- **👤 Customers** → Manages user profiles.

🔹 **Asynchronous Order Processing** is managed with **Celery** and **RabbitMQ**.
🔹 **MySQL** serves as the primary relational database for structured data storage.

### **2️⃣ Infrastructure & Deployment**
- **Docker & Docker Compose** facilitate containerized application deployment.
- **AWS Hosting** leveraging:
  - **EC2** for compute power.
  - **RDS (MySQL)** for database management.

---

## 📊 Logging & Monitoring

### **1️⃣ ELK Stack for Centralized Logging**
- **Elasticsearch** → Stores structured logs for efficient querying and analytics.
- **Logstash** → Processes application logs before forwarding them to Elasticsearch.
- **Kibana** → Provides an interactive UI for log visualization and monitoring.
- **Filebeat** → Collects and streams logs from microservices.

### **2️⃣ Metrics & Performance Monitoring**
- **RabbitMQ Monitoring** → Tracks queue performance and bottlenecks.

---

## ⚙️ API Design & Documentation
The API is designed following **RESTful best practices**, ensuring **scalability and maintainability**.

🔹 **Swagger UI & OpenAPI Specification** provide interactive documentation for seamless integration.

### **API Endpoints**
| Method | Endpoint               | Description            |
|--------|------------------------|------------------------|
| `GET`  | `/api/v1/metrics/`     | Retrieve order metrics |
| `POST` | `/api/v1/orders/`      | Create a new order     |
| `GET`  | `/api/v1/orders/{id}/` | Retrieve order details |

---

## 🔄 Order Processing Workflow
1. **Order Placement** → Customers place orders via the frontend.
2. **Asynchronous Processing** → Orders are queued and processed using Celery workers.
3. **Inventory & Verification** → Ensures stock availability and transaction success.
4. **Real-Time Order Tracking** → Customers receive live status updates.

---

## 🚀 Setup & Deployment Guide

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/vishwajeetverma613/Par-Cart/tree/dev-vv
git fetch --all
git checkout dev-vv
cd ecommerce-backend
```

### **2️⃣ Configure Environment Variables**
Create a `.env` file with the following:
```ini
DATABASE_URL=mysql://username:password@db_host:3306/db_name
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://rabbitmq:5672/
ELASTICSEARCH_URL=http://elasticsearch:9200
```

### **3️⃣ Run the Services**
```bash
docker-compose up -d --build
docker-compose -f docker-compose-queue.yml up -d --build
```

### **4️⃣ Run Database Migrations**
```bash
DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py makemigrations
DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py migrate
```

### **5️⃣ Create a Superuser for Admin Access**
```bash
DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py createsuperuser
```

### **6️⃣ Access the Application**
- **API Server** → [http://13.201.1.102:8000/api/v1/]
- **Admin Panel** → [http://13.201.1.102:8000/admin/] *(guest / fuVUhqMt9t5j2ev)*
- **Swagger UI** → [http://13.201.1.102:8000/swagger/]
- **RabbitMQ Admin** → [http://13.201.1.102:15672/] *(guest_viewer / user_paskjnknks)*
- **Kibana Dashboard** → [http://13.201.1.102:5601/]

---

## 🛠️ Logging & Monitoring Setup

### **1️⃣ ELK Stack Setup**
Deploy Elasticsearch, Logstash, and Kibana via Docker Compose:
```bash
docker-compose -f elk-stack-compose.yml up -d
```

### **2️⃣ Filebeat Configuration**
Configure **Filebeat** to forward logs to **Logstash**:
```yml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/django/*.log
output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

### **🔟 Logstash Configuration**
Configure **Logstash** to forward logs to **ELasticsearch**:
Paste the above to logstash.conf file
```conf
input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "ecommerce-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}


---

## 🎯 Final Thoughts
The **E-Commerce Backend System** is built for performance, scalability, and real-time monitoring. With a microservices-based architecture, robust logging, and containerized deployment, this solution is designed to handle high traffic, ensuring a seamless shopping experience for users. 🚀

🔹 GitHub Repository & Deployment Details
GitHub Repo: Par-Cart Backend
Public API Endpoint: [http://13.201.1.102:8000/api/v1/]
