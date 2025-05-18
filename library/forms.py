from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    # Форма для створення та редагування відгуків про книги
    class Meta:
        model = Review
        fields = ['text', 'rating']  # Поля які відображатимуться у формі
        # Кастомні віджети для стилізації форми
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }
        # Українські назви полів
        labels = {
            'text': 'Ваш відгук',
            'rating': 'Оцінка'
        }