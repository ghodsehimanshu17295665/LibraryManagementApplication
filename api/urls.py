from django.urls import path
from .views import (
    AuthorView,
    CategoryView,
    BookView,
    CourseView,
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
    path('authors/', AuthorView.as_view(), name='author-list-create'),
    path('authors/<uuid:pk>/', AuthorView.as_view(), name='author-detail'),
    path('categories/', CategoryView.as_view(), name='categories-list-create'),
    path('categories/<uuid:pk>/', CategoryView.as_view(), name='categories-detail'),
    path('books/', BookView.as_view(), name='books-list-create'),
    path('books/<uuid:pk>/', BookView.as_view(), name='books-detail'),
    path('courses/', CourseView.as_view(), name='course-list-create'),
    path('courses/<uuid:pk>/', CourseView.as_view(), name='course-detail'),

    path(
        "students/register/",
        StudentRegistrationAPIView.as_view(),
        name="student-register",
    ),
    path(
        "students/login/", StudentLoginAPIView.as_view(), name="student-login"
    ),
    path(
        "students/logout/",
        StudentLogoutAPIView.as_view(),
        name="student-logout",
    ),
    path(
        "students/<uuid:pk>/",
        StudentRetrieveUpdateAPIView.as_view(),
        name="student-detail-update",
    ),
    path("students/", StudentListAPIView.as_view(), name="student-list"),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("issue-book/", IssueBookView.as_view(), name="issue-book"),
    path("return-book/", ReturnBookView.as_view(), name="return-book"),
    path("issued-books/", IssuedBookListView.as_view(), name="issued-books"),
]


# author/create/
# author/update/
# author/list/
# author/retireve
# urlpatterns = [
#     path('authors/', AuthorView.as_view(), name='author-list-create'),
#     path('authors/<int:pk>/', AuthorView.as_view(), name='author-detail'),
# ]
