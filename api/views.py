from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.timezone import now
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Author, Category, Book, Course, Student, IssuedBook
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    CourseSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    StudentLoginSerializer,
    IssuedBookSerializer,
    ReturnBookSerializer,
)
from .pagination import (
    CategoryPagination,
    BookPagination,
    CoursePagination,
    StudentPagination,
    IssuedBookPagination,
)
from .filters import BookFilter, AuthorFilter, CategoryFilter, IssuedBookFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from datetime import datetime, timedelta


# List and Create Author :-
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Create a success message
        return Response({
            'message': 'Author created successfully!',
            'author': serializer.data
        }, status=status.HTTP_201_CREATED)


# Retrieve, Update, and Delete
class AuthorRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# List and Create Category
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ["title", "publication_date", "quantity"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if Book.objects.filter(title=serializer.initial_data.get('title')).exists():
            return Response(
                {'error': 'A book with this title already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Retrive, Update, and Delete Book
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# List and Create API for Course (With Pagination)
class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# Retrieve, Update, and Delete API for Course
class CourseRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# Student Registration (SignUp API)
class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer


# Login view
class StudentLoginAPIView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Generate the JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return tokens and success message
        return Response(
            {
                "message": "Successfully logged in!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )


# Logout view
class StudentLogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({"message": "Successfully logged out!"}, status=200)


# Retrieve and Update Student Information
# class StudentRetrieveUpdateAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         student = Student.objects.get(pk=pk)
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)

#     def put(self, request, pk, *args, **kwargs):
#         student = Student.objects.get(pk=pk)
#         serializer = StudentSerializer(student, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message': 'Student information updated successfully!',
#                 'data': serializer.data
#             }, status=200)
#         return Response(serializer.errors, status=400)

class StudentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


# Get All Students with Pagination
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "message": "Students retrieved successfully!",
                "data": response.data,
            }
        )


class IssueBookView(generics.CreateAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer


class ReturnBookView(generics.GenericAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = ReturnBookSerializer

    def post(self, request, *args, **kwargs):
        # Validate and serialize the input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call the save method, which will handle the logic in the serializer
        serializer.save(student=request.user)

        return Response(
            {"message": "Book returned successfully."},
            status=status.HTTP_200_OK,
        )


class IssuedBookListView(generics.ListAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    pagination_class = IssuedBookPagination
    filterset_class = IssuedBookFilter

    def get_queryset(self):
        return IssuedBook.objects.filter(is_returned=False)


# class IssueBookView(APIView):
#     def post(self, request, *args, **kwargs):
#         book_id = request.data.get("book")  # This is String

#         # Get the book Object
#         book = Book.objects.filter(id=book_id).first()
#         if not book:
#             return Response(
#                 {"msg": "Book Not Found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         student = request.user  # This is user Objects
#         if not student:
#             return Response(
#                 {"msg": "Student Not Found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         # Check if the book is already issued and not returned
#         is_book_issued = IssuedBook.objects.filter(
#             book=book, student=student, is_returned=False
#         )

#         if book.quantity <= 0:
#             return Response(
#                 {"msg": "No Book available to issue"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         book.quantity -= 1
#         book.save()

#         if is_book_issued:
#             return Response(
#                 {"msg": "Book is already issued"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         issued_book = IssuedBook(
#             book=book,
#             student=student,
#             issue_date=datetime.now(),
#             due_date=datetime.now() + timedelta(days=10),
#             is_returned=False,
#         )

#         issued_book.save()

#         return Response(
#             {
#                 "id": issued_book.id,
#                 "book": issued_book.book.id,
#                 "student": issued_book.student.id,
#                 "issue_date": issued_book.issue_date,
#                 "due_date": issued_book.due_date,
#                 "is_returned": issued_book.is_returned,
#             },
#             status=status.HTTP_201_CREATED,
#         )


# class ReturnBookView(APIView):
#     def post(self, request, *args, **kwargs):
#         issued_book_id = request.data.get("issued_book")

#         # Get the issued book
#         issued_book = IssuedBook.objects.filter(id=issued_book_id).first()

#         if not issued_book:
#             return Response(
#                 {"msg": "Issued book record not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         student = request.user
#         if not student:
#             return Response(
#                 {"msg": "User not authenticated"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         # Check if the book has already been returned
#         if issued_book.is_returned:
#             return Response(
#                 {"msg": "This book has already been returned."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Mark the book as returned
#         issued_book.is_returned = True
#         issued_book.return_date = now().date()
#         issued_book.save()

#         # Get the associated book and increase the quantity
#         book = issued_book.book
#         book.quantity += 1
#         book.save()

#         return Response(
#             {"message": "Book returned successfully."},
#             status=status.HTTP_200_OK,
#         )
