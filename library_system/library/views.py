from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Q
from .models import Book, Genre, Review, Favorite, ReadingHistory
from .forms import ReviewForm
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.timezone import now, timedelta
from django.db import IntegrityError


def home(request):
    books = Book.objects.filter(available=True)[:6]
    genres = Genre.objects.all()
    return render(request, 'library/home.html', {
        'books': books,
        'genres': genres
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обліковий запис створено! Тепер ви можете увійти.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def book_list(request):
    genre_id = request.GET.get('genre')
    search_query = request.GET.get('query')

    books = Book.objects.all()

    if genre_id:
        books = books.filter(genre_id=genre_id)

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    genres = Genre.objects.all()

    return render(request, 'library/book_list.html', {
        'books': books,
        'genres': genres,
        'current_genre': int(genre_id) if genre_id else None,
        'search_query': search_query
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(book=book, user=request.user).exists()

    one_day_ago = now() - timedelta(days=1)
    if not ReadingHistory.objects.filter(book=book, user=request.user, read_at__gte=one_day_ago).exists():
        ReadingHistory.objects.create(book=book, user=request.user)

    return render(request, 'library/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'is_favorite': is_favorite,
        'form': ReviewForm()
    })


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()
        else:
            form = ReviewForm()
        if form.is_valid():
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            if existing_review:
                existing_review.text = form.cleaned_data['text']
                existing_review.rating = form.cleaned_data['rating']
                existing_review.save()
                messages.success(request, 'Ваш відгук оновлено!')
            else:
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, 'Ваш відгук додано!')

    return redirect('book_detail', book_id=book_id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        messages.error(request, 'Ви не можете видалити цей відгук!')
        return redirect('book_detail', book_id=review.book.id)

    book_id = review.book.id
    review.delete()
    messages.success(request, 'Відгук видалено!')

    return redirect('book_detail', book_id=book_id)


@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    try:
        favorite, created = Favorite.objects.get_or_create(book=book, user=request.user)
    except IntegrityError:
        favorite = Favorite.objects.get(book=book, user=request.user)
        created = False

    if created:
        messages.success(request, 'Книгу додано до улюблених!')
    else:
        messages.info(request, 'Ця книга вже є у вашому списку улюблених.')

    return redirect('book_detail', book_id=book_id)


@login_required
def remove_from_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite = get_object_or_404(Favorite, book=book, user=request.user)
    favorite.delete()

    messages.success(request, 'Книгу видалено з улюблених!')
    return redirect('book_detail', book_id=book_id)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')

    return render(request, 'library/favorites.html', {
        'favorites': favorites
    })


@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(user=request.user).select_related('book')

    return render(request, 'library/reading_history.html', {
        'history': history
    })


@login_required
def download_book_pdf(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    pdfmetrics.registerFont(
        TTFont('DejaVuSans', 'FreeSans.ttf'))

    p.setFont('DejaVuSans', 14)
    p.drawString(1 * inch, 10 * inch, f"Книга: {book.title}")
    p.setFont('DejaVuSans', 12)
    p.drawString(1 * inch, 9.5 * inch, f"Автор: {book.author}")

    if book.genre:
        p.drawString(1 * inch, 9 * inch, f"Жанр: {book.genre.name}")

    p.setFont('DejaVuSans', 10)
    desc_lines = book.description.replace('\r\n', '\n').split('\n')
    y_position = 8 * inch

    for line in desc_lines:
        while len(line) > 90:
            p.drawString(1 * inch, y_position, line[:90])
            line = line[90:]
            y_position -= 0.25 * inch

        p.drawString(1 * inch, y_position, line)
        y_position -= 0.25 * inch

    p.showPage()
    p.save()

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"{book.title}.pdf")