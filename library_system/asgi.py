import os
from django.core.asgi import get_asgi_application

# Налаштування модуля настройок Django для ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

# Створення ASGI додатку для асинхронного обслуговування запитів
application = get_asgi_application()