from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Book, Genre, Review, Favorite, ReadingHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'available')
    list_filter = ('available', 'genre')
    search_fields = ('title', 'author')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'added_at')


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'read_at')
    list_filter = ('read_at',)


class CustomUserAdmin(BaseUserAdmin):
    actions = ['reset_password']

    def reset_password(self, request, queryset):
        for user in queryset:
            user.set_password('new_password')
            user.save()
        self.message_user(request, f"Пароль змінено для {queryset.count()} користувачів")

    reset_password.short_description = "Змінити пароль вибраним користувачам"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
