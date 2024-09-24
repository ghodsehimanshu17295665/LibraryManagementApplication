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
    StudentLoginAPIView,
    StudentLogoutAPIView,
    StudentRetrieveUpdateAPIView,
    StudentListAPIView,
    IssueBookView,
    ReturnBookView,
    IssuedBookListView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
    path('students/register/', StudentRegistrationAPIView.as_view(), name='student-register'),
    path('students/login/', StudentLoginAPIView.as_view(), name='student-login'),
    path('students/logout/', StudentLogoutAPIView.as_view(), name='student-logout'),
    path('students/<uuid:pk>/', StudentRetrieveUpdateAPIView.as_view(), name='student-detail-update'),
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('issue-book/', IssueBookView.as_view(), name='issue-book'),
    path('return-book/', ReturnBookView.as_view(), name='return-book'),
    path('issued-books/', IssuedBookListView.as_view(), name='issued-books'),
]
