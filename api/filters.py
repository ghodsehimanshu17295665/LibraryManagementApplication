import django_filters
from .models import Book, IssuedBook


class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name="author__name", lookup_expr="icontains"
    )
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )

    class Meta:
        model = Book
        fields = ["author", "category"]


class IssuedBookFilter(django_filters.FilterSet):
    """
    Filter issued books by student or book.
    """
    student = django_filters.CharFilter(field_name='student__name', lookup_expr='icontains')
    book = django_filters.CharFilter(field_name='book__title', lookup_expr='icontains')

    class Meta:
        model = IssuedBook
        fields = ['student', 'book']
