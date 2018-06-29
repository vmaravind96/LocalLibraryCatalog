from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic

# Create your views here.


def index(request):
    """
    Home page of our Library Application
    Args:
        request: HttpRequest

    Returns:
        template
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_fiction = Genre.objects.filter(name__iexact='fiction').count()

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_fiction': num_fiction},
    )


class BookListView(generic.ListView):
    """
    List view for displaying the books available
    """
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    """
    Detail view for getting a particular book details
    """
    model = Book


class AuthorListView(generic.ListView):
    """
    List view for authors available
    """
    model = Author
    paginate_by = 3


class AuthorDetailView(generic.DetailView):
    """
    Detail view for getting a particular book details
    """
    model = Author
