import os
from django.core.wsgi import get_wsgi_application

# Налаштування модуля настройок Django для WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

# Створення WSGI додатку для синхронного обслуговування HTTP-запитів
application = get_wsgi_application()