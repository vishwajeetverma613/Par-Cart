from celery import Celery

app = Celery("ecommerce")  # Your Django project name
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
