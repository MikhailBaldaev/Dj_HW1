from django.shortcuts import redirect, render, get_object_or_404
from books.models import Book


def index(request):

    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books_list': books}

    return render(request, template, context)


def book_date(request, pub_date):
    book = get_object_or_404(Book, pub_date=pub_date)

    try:
        book.get_previous_by_pub_date()
        previous_book = book.get_previous_by_pub_date()
    except:
        previous_book = None

    try:
        book.get_next_by_pub_date()
        next_book = book.get_next_by_pub_date()
    except:
        next_book = None

    template = 'books/book_date.html'
    context = {
        'book': book,
        'previous': previous_book,
        'next': next_book,
    }

    return render(request, template, context)
