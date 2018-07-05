from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Book, BookInstance, Author, Genre
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RenewBookForm

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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10
    permission_required = 'catalog.staff_permission_required'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# Renew book view (Form based)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

# Author views for models added


class AuthorCreate(CreateView):
    """
    Creating an author
    """
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}


class AuthorUpdate(UpdateView):
    """
    Update details for existing author
    """
    model = Author
    fields = ['first_name','last_name','date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    """
    Deleting existing author
    """
    model = Author
    success_url = reverse_lazy('authors')

# Book create, delete and modify


class BookCreate(CreateView):
    """
    Creating a book
    """
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    """
    Update existing book details
    """
    model = Book
    fields = ['author', 'summary', 'isbn', 'genre']


class BookDelete(DeleteView):
    """
    Delete the book
    """
    model = Book
    success_url = reverse_lazy('books')

