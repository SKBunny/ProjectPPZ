from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/add_review/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('books/<int:book_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('books/<int:book_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('history/', views.reading_history, name='reading_history'),
    path('books/<int:book_id>/download_pdf/', views.download_book_pdf, name='download_book_pdf'),
    path('register/', views.register, name='register'),
]