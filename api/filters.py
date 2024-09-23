import django_filters
from .models import Book


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
