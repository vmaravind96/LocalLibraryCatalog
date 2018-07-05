from django.contrib import admin

from .models import Book, BookInstance, Author, Genre

# Register your models here.

# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)

# Define the admin class


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin model for author
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin for BOOK
    """
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """
    Admin for BookInstance
    """
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
