from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from .models import Author, Category, Book, Course, Student
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    CourseSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
)
from .pagination import (
    CategoryPagination,
    BookPagination,
    CoursePagination,
    StudentPagination,
)
from .filters import BookFilter
from rest_framework.permissions import IsAdminUser, AllowAny


# List and Create Author :-
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Retrieve, Update, and Delete
class AuthorRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# List and Create Category
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


# Retrieve, Update, and Delete Category
class CategoryRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# List and Create Books
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# Retrive, Update, and Delete Book
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# List and Create API for Course (With Pagination)
class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [IsAdminUser]


# Retrieve, Update, and Delete API for Course
class CourseRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]


# Student Registration (SignUp API)
class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [AllowAny]


# Retrieve and Update Student Information
class StudentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


# Get All Students with Pagination
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination  # Apply custom pagination
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Only authenticated users can view
