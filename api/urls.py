from django.urls import path
from .views import (
    AuthorListCreateAPIView,
    AuthorRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    StudentRegistrationAPIView,
    StudentRetrieveUpdateAPIView,
    StudentListAPIView,
)


urlpatterns = [
    path(
        "authors/",
        AuthorListCreateAPIView.as_view(),
        name="author-list-create",
    ),
    path(
        "authors/<uuid:pk>/",
        AuthorRetrieveUpdateDestroyAPIView.as_view(),
        name="author-detail",
    ),
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<uuid:pk>/",
        CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category-detail",
    ),
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path(
        "books/<uuid:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
        name="book-detail",
    ),
    path(
        "courses/",
        CourseListCreateAPIView.as_view(),
        name="course-list-create",
    ),
    path(
        "courses/<uuid:pk>/",
        CourseRetrieveUpdateDestroyAPIView.as_view(),
        name="course-detail",
    ),
    path(
        "students/register/",
        StudentRegistrationAPIView.as_view(),
        name="student-register",
    ),
    path(
        "students/<uuid:pk>/",
        StudentRetrieveUpdateAPIView.as_view(),
        name="student-detail-update",
    ),
    path("students/", StudentListAPIView.as_view(), name="student-list"),
]
