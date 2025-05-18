from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Book, Genre, Review, Favorite, ReadingHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Налаштування відображення книг в адмін-панелі
    list_display = ('title', 'author', 'genre', 'available')
    list_filter = ('available', 'genre')  # Фільтри для швидкого пошуку
    search_fields = ('title', 'author')  # Поля для пошуку


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Простий список жанрів в адмін-панелі
    list_display = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Налаштування відображення відгуків в адмін-панелі
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating',)  # Фільтр за рейтингом


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    # Налаштування відображення обраних книг в адмін-панелі
    list_display = ('book', 'user', 'added_at')


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    # Налаштування відображення історії читання в адмін-панелі
    list_display = ('book', 'user', 'read_at')
    list_filter = ('read_at',)  # Фільтр за датою прочитання


class CustomUserAdmin(BaseUserAdmin):
    # Розширена адмін-панель для користувачів з додатковими діями
    actions = ['reset_password']

    def reset_password(self, request, queryset):
        # Масове скидання паролю для вибраних користувачів
        for user in queryset:
            user.set_password('new_password')
            user.save()
        self.message_user(request, f"Пароль змінено для {queryset.count()} користувачів")

    reset_password.short_description = "Змінити пароль вибраним користувачам"


# Заміна стандартної адмін-панелі користувачів на кастомну
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)