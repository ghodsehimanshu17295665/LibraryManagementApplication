from django_filters.rest_framework import DjangoFilterBackend
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
)
from .pagination import (
    CategoryPagination,
    BookPagination,
    CoursePagination,
    StudentPagination,
    IssuedBookPagination,
)
from .filters import BookFilter, IssuedBookFilter
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


# Login view
class StudentLoginAPIView(generics.GenericAPIView):
    serializer_class = StudentLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Generate the JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return tokens and success message
        return Response({
            'message': 'Successfully logged in!',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)


# Logout view
class StudentLogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({
            'message': 'Successfully logged out!'
        }, status=200)


# Retrieve and Update Student Information
class StudentRetrieveUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Student information updated successfully!',
                'data': serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)


# Get All Students with Pagination
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'message': 'Students retrieved successfully!',
            'data': response.data
        })


class IssueBookView(APIView):
    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        student_id = request.data.get('student')

        # Check if the book is already issued and not returned
        if IssuedBook.objects.filter(book_id=book_id, is_returned=False).exists():
            return Response({"error": "Book is already issued to another student."}, status=status.HTTP_400_BAD_REQUEST)

        # If available, issue the book
        serializer = IssuedBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    def post(self, request, *args, **kwargs):
        issued_book_id = request.data.get('issued_book')

        try:
            issued_book = IssuedBook.objects.get(id=issued_book_id, is_returned=False)
            issued_book.is_returned = True
            issued_book.return_date = now().date()
            issued_book.save()
            return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
        except IssuedBook.DoesNotExist:
            return Response({"error": "Issued book not found or already returned."}, status=status.HTTP_404_NOT_FOUND)


class IssuedBookListView(generics.ListAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    pagination_class = IssuedBookPagination
    filterset_class = IssuedBookFilter
