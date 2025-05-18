from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Основні URL-маршрути проекту бібліотечної системи
urlpatterns = [
    path('admin/', admin.site.urls),           # Адміністративна панель Django
    path('', include('library.urls')),         # Включення URL додатку library (головна сторінка)
    path('accounts/', include('django.contrib.auth.urls')),  # Стандартні URL для аутентифікації (login, logout тощо)
]