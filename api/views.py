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
from .decorators import custom_permission
from django.shortcuts import get_object_or_404


class AuthorView(generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

    def get_objects(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrieve a single author
            author = self.get_object()
            serializer = self.get_serializer(author)
            return Response(serializer.data)
        else:
            # List all authors
            authors = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(authors, many=True)
            return Response(serializer.data)

    @custom_permission
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Author created successfully!',
            'author': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    @custom_permission
    def put(self, request, *args, **kwargs):
        author = self.get_object()
        serializer = self.get_serializer(author, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return response with success message and updated author data
        return Response({
            'message': 'Author updated successfully!',
            'author': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    @custom_permission
    def patch(self, request, *args, **kwargs):
        author = self.get_object()
        serializer = self.get_serializer(author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Author partially updated successfully!',
            'author': serializer.data
        }, status=status.HTTP_200_OK)

    @custom_permission
    def delete(self, request, *args, **kwargs):
        author = self.get_object()  # Retrieve the author object
        self.perform_destroy(author)  # Perform the deletion

        # Return response with success message
        return Response({
            'message': 'Author deleted successfully!'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CategoryView(generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = CategoryFilter

    def get_objects(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrieve a single category
            category = self.get_object()
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        else:
            # List all categories
            categories = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)

    @custom_permission
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Category created successfully!',
            'category': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    @custom_permission
    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Category updated successfully!',
            'category': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    @custom_permission
    def patch(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Category partially updated successfully!',
            'category': serializer.data
        }, status=status.HTTP_200_OK)

    @custom_permission
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        self.perform_destroy(category)

        return Response({
            'message': 'Category deleted successfully!'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class BookView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ["title", "publication_date", "quantity"]

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrive a  Single Book.
            book = self.get_object()
            serializer = self.get_serializer(book)
            return Response(serializer.data)
        else:
            # List all Books
            books = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

    @custom_permission
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Book Created Successfully!',
            'book': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    @custom_permission
    def put(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Book Updated Successfully!',
            'book': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    @custom_permission
    def patch(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Book Partially update Successfully!',
            'book': serializer.data
        }, status=status.HTTP_200_OK)

    @custom_permission
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        self.perform_destroy(book)

        return Response({
            'message': 'Book deleted Successfully!'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CourseView(generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwarg.get('pk'))

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrive a Single Course
            course = self.get_object()
            serializer = self.get_serializer(course)
            return Response(serializer.data)
        else:
            # List All Courses
            courses = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(courses, many=True)
            return Response(serializer.data)

    @custom_permission
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Course Created Successfully!',
            'course': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    @custom_permission
    def put(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Course Updated Successfully!',
            'course': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
    
    @custom_permission
    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Course Updated Partially Successfully!',
            'course': serializer.data
        }, status=status.HTTP_200_OK)

    @custom_permission
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        self.perform_destroy(book)

        return Response({
            'message': 'Book deleted Successfully!'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()






# # List and Create API for Course (With Pagination)
# class CourseListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     pagination_class = CoursePagination

#     @custom_permission
#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # Retrieve, Update, and Delete API for Course
# class CourseRetrieveUpdateDestroyAPIView(
#     generics.RetrieveUpdateDestroyAPIView
# ):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     @custom_permission
#     def update(self, request, *args, **kwargs):
#         return super().update(request, *args, **kwargs)

#     @custom_permission
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


# Student Registration (SignUp API)
class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer


# Login view
class StudentLoginAPIView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentLoginSerializer

    def post(self, request):
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

    def post(self, request):
        return Response({"message": "Successfully logged out!"}, status=200)


class StudentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, **kwargs):
        # Get the student instance that is being accessed
        student = self.get_object()

        # Check if the authenticated user matches the student
        if student.id == request.user.id:
            # Perform the deletion
            student.delete()
            return Response({"message": "Student deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You do not have permission to delete this student."},
                            status=status.HTTP_403_FORBIDDEN)


# Get All Students with Pagination
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        response = super().list(request)
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

    def post(self, request):
        # Validate and serialize the input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call the save method, which will handle the logic in the serializer
        issued_book = serializer.save(student=request.user)

        return Response(
            {"message": "Book returned successfully!", "issued_book_id": issued_book.id},
            status=status.HTTP_200_OK
        )


class IssuedBookListView(generics.ListAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    pagination_class = IssuedBookPagination
    filterset_class = IssuedBookFilter

    def get_queryset(self):
        return IssuedBook.objects.filter(is_returned=False)
