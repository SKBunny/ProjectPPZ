from pathlib import Path

# Базовий шлях проекту для побудови інших шляхів
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ПОПЕРЕДЖЕННЯ: тримайте секретний ключ у таємниці в продакшені!
SECRET_KEY = 'django-insecure-m-)90qgb&#ivwy4qj&n2fyv&-t!)+5-g$hwwcc&mw454uvdvhj'

# ПОПЕРЕДЖЕННЯ: не запускайте з DEBUG=True в продакшені!
DEBUG = True

# Дозволені хости для доступу до додатку
ALLOWED_HOSTS = []


# Визначення додатків

INSTALLED_APPS = [
    'django.contrib.admin',          # Адміністративна панель
    'django.contrib.auth',           # Система аутентифікації
    'django.contrib.contenttypes',   # Типи контенту
    'django.contrib.sessions',       # Управління сесіями
    'django.contrib.messages',       # Система повідомлень
    'django.contrib.staticfiles',    # Обробка статичних файлів
    'library_system',                # Основний проект
    'library'                        # Додаток бібліотеки
]

# Проміжне програмне забезпечення (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Безпека
    'django.contrib.sessions.middleware.SessionMiddleware',   # Сесії
    'django.middleware.common.CommonMiddleware',              # Загальне middleware
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF захист
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Аутентифікація
    'django.contrib.messages.middleware.MessageMiddleware',   # Повідомлення
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Захист від clickjacking
]

# Основний модуль URL конфігурації
ROOT_URLCONF = 'library_system.urls'

# Налаштування шаблонів
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                    # Директорії для пошуку шаблонів
        'APP_DIRS': True,              # Пошук шаблонів в додатках
        'OPTIONS': {
            'context_processors': [    # Процесори контексту для шаблонів
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI додаток для синхронного обслуговування
WSGI_APPLICATION = 'library_system.wsgi.application'


# База даних
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Використання SQLite
        'NAME': BASE_DIR / 'db.sqlite3',         # Шлях до файлу БД
    }
}


# Валідація паролів
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Перевірка схожості з атрибутами користувача
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Перевірка мінімальної довжини паролю
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Перевірка на загальні паролі
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Перевірка на числові паролі
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Інтернаціоналізація
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Код мови за замовчуванням

TIME_ZONE = 'UTC'        # Часовий пояс

USE_I18N = True          # Включити інтернаціоналізацію

USE_TZ = True            # Використовувати часові пояси


# Статичні файли (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Тип первинного ключа за замовчуванням
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


import os

# Налаштування статичних файлів
STATIC_URL = '/static/'                                    # URL для статичних файлів
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')      # Папка для збирання статичних файлів
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]    # Додаткові директорії зі статичними файлами

# Налаштування медіа файлів (завантажених користувачами)
MEDIA_URL = '/media/'          # URL для медіа файлів
MEDIA_ROOT = BASE_DIR / 'media' # Папка для збереження медіа файлів

# Перенаправлення після входу/виходу
LOGIN_REDIRECT_URL = 'home'    # Сторінка після успішного входу
LOGOUT_REDIRECT_URL = 'home'   # Сторінка після виходу

# Налаштування Bootstrap класів для повідомлень Django
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}