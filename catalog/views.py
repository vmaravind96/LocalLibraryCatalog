from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_fiction': num_fiction, 'num_visits': num_visits},
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


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

