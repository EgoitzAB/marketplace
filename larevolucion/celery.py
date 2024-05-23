import os
from celery import Celery

# establecer el módulo por defecto para el programa celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'larevolucion.settings')

app = Celery('larevolucion')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
