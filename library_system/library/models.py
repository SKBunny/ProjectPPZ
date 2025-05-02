from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import UniqueConstraint


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва жанру")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    author = models.CharField(max_length=200, verbose_name="Автор")
    description = models.TextField(verbose_name="Опис")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Жанр")
    available = models.BooleanField(default=True, verbose_name="В наявності")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Дата видання")
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name="Обкладинка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Користувач")
    text = models.TextField(verbose_name="Текст відгуку")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оцінка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Відгук на {self.book.title} від {self.user.username}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ['-created_at']
        unique_together = ['book', 'user']


class Favorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorites', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Користувач")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} в обраному у {self.user.username}"

    class Meta:
        verbose_name = "Обране"
        verbose_name_plural = "Обране"
        constraints = [
            UniqueConstraint(fields=['book', 'user'], name='unique_review')
        ]

class ReadingHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='history', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history', verbose_name="Користувач")
    read_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} прочитав {self.book.title}"

    class Meta:
        verbose_name = "Історія читання"
        verbose_name_plural = "Історія читання"
        ordering = ['-read_at']