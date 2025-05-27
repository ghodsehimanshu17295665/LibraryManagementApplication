import django_filters
from .models import Book, IssuedBook, Author, Category
from django_filters import rest_framework as filters


# Filter for Author model
class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="name", lookup_expr="icontains")
    nationality = filters.CharFilter(
        field_name="nationality", lookup_expr="icontains"
    )

    class Meta:
        model = Author
        fields = ["name", "email", "nationality"]


# Filter for Category model
class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    description = filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )

    class Meta:
        model = Category
        fields = ["name", "description"]


# Filter for Book model
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters.CharFilter(
        field_name="author__name", lookup_expr="icontains"
    )
    category = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    publication_date = filters.DateFilter(
        field_name="publication_date", lookup_expr="exact"
    )
    min_quantity = filters.NumberFilter(
        field_name="quantity", lookup_expr="gte"
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "publication_date",
            "quantity",
        ]


class IssuedBookFilter(django_filters.FilterSet):
    """
    Filter issued books by student or book.
    """

    student = django_filters.CharFilter(
        field_name="student__name", lookup_expr="icontains"
    )
    book = django_filters.CharFilter(
        field_name="book__title", lookup_expr="icontains"
    )

    class Meta:
        model = IssuedBook
        fields = ["student", "book"]
