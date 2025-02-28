# Use a lightweight Python Alpine image
FROM python:3.11-alpine


# Set working directory
WORKDIR /app

# Install dependencies
RUN apk update && apk add --no-cache \
    gcc g++ musl-dev \
    mariadb-dev  \
    python3-dev \
    libffi-dev \
    && pip install --upgrade pip

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ecommerce_service.settings python manage.py runserver 0.0.0.0:8000"]
