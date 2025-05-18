from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import UniqueConstraint


class Genre(models.Model):
    # Модель для жанрів книг
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва жанру")

    def __str__(self):
        # Повертає назву жанру як рядкове представлення
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Book(models.Model):
    # Основна модель для книг в бібліотечній системі
    title = models.CharField(max_length=200, verbose_name="Назва")
    author = models.CharField(max_length=200, verbose_name="Автор")
    description = models.TextField(verbose_name="Опис")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Жанр")
    available = models.BooleanField(default=True, verbose_name="В наявності")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Дата видання")
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name="Обкладинка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Повертає назву та автора книги як рядкове представлення
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        # Повертає URL для детальної сторінки книги
        return reverse('book_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']  # Сортування за датою створення (найновіші спочатку)


class Review(models.Model):
    # Модель для відгуків користувачів про книги
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Користувач")
    text = models.TextField(verbose_name="Текст відгуку")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оцінка")  # Рейтинг від 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Повертає опис відгуку
        return f"Відгук на {self.book.title} від {self.user.username}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ['-created_at']  # Сортування за датою створення (найновіші спочатку)
        unique_together = ['book', 'user']  # Один відгук від користувача на одну книгу


class Favorite(models.Model):
    # Модель для збереження обраних книг користувачами
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorites', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Користувач")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Повертає опис обраної книги
        return f"{self.book.title} в обраному у {self.user.username}"

    class Meta:
        verbose_name = "Обране"
        verbose_name_plural = "Обране"
        constraints = [
            # Унікальне обмеження: одна книга може бути в обраному у користувача тільки одного разу
            UniqueConstraint(fields=['book', 'user'], name='unique_review')
        ]

class ReadingHistory(models.Model):
    # Модель для збереження історії прочитаних книг
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='history', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history', verbose_name="Користувач")
    read_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Повертає опис прочитаної книги
        return f"{self.user.username} прочитав {self.book.title}"

    class Meta:
        verbose_name = "Історія читання"
        verbose_name_plural = "Історія читання"
        ordering = ['-read_at']  # Сортування за датою прочитання (найновіші спочатку)