from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

# URL-маршрути для бібліотечної системи
urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка
    path('books/', views.book_list, name='book_list'),  # Список всіх книг
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),  # Детальна сторінка книги
    path('books/<int:book_id>/add_review/', views.add_review, name='add_review'),  # Додавання відгуку
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),  # Видалення відгуку
    path('books/<int:book_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),  # Додавання в обране
    path('books/<int:book_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),  # Видалення з обраного
    path('favorites/', views.favorites_list, name='favorites_list'),  # Список обраних книг
    path('history/', views.reading_history, name='reading_history'),  # Історія читання
    path('books/<int:book_id>/download_pdf/', views.download_book_pdf, name='download_book_pdf'),  # Завантаження PDF
    path('register/', views.register, name='register'),  # Реєстрація користувача
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Вихід з аккаунту
]

# Налаштування для обслуговування медіа файлів у режимі розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)