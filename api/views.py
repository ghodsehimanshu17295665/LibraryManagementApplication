from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.timezone import now
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
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
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

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
        # Fetch the course object using get_object()
        course = self.get_object()

        # Pass the course object and the updated data to the serializer
        serializer = self.get_serializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform the update
        self.perform_update(serializer)

        # Return a success message along with the updated course data
        return Response({
            'message': 'Course Updated Successfully!',
            'course': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        # Save the updates to the course
        serializer.save()

    # Add a get_object method to retrieve the course instance by its pk (UUID)
    def get_object(self):
        # Use get_object_or_404 to get the course based on the UUID pk
        return get_object_or_404(Course, pk=self.kwargs['pk'])

    @custom_permission
    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Course Updated Partially Successfully!',
            'course': serializer.data
        }, status=status.HTTP_200_OK)

    @custom_permission
    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        self.perform_destroy(course)

        return Response({
            'message': 'Course deleted Successfully!'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


# Student Registration (SignUp API)
class StudentRegistrationAPIView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        return Response({
            'message': 'Student registered successfully!',
            'student': self.get_serializer(student).data
        }, status=status.HTTP_201_CREATED)


# Login view
class StudentLoginLogoutAPIView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        action = self.kwargs.get('action')

        if action == 'login':
            return self.handle_login(request)
        elif action == 'logout':
            return self.handle_logout(request)
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

    def handle_login(self, request):
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
            status=status.HTTP_200_OK,
        )

    def handle_logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the access token
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentAPIView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            student = self.get_object()
            serializer = self.get_serializer(student)
            return Response({
                "message": "Student retrieved successfully!",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            # List All Students
            students = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(students)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(students, many=True)
            return Response({
                "message": "Students retrieved successfully!",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Student Updated Successfully!',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def patch(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Student Partially Updated Successfully!',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        student = self.get_object()

        # Check if the authenticated user matches the student
        if student.id == request.user.id:
            # Perform the deletion
            student.delete()
            return Response({"message": "Student deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You do not have permission to delete this student."},
                            status=status.HTTP_403_FORBIDDEN)


class IssuedBookView(generics.GenericAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    pagination_class = IssuedBookPagination
    filterset_class = IssuedBookFilter
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Book Issued Successfully!',
            'course': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        issued_books = self.filter_queryset(self.get_queryset().filter(is_returned=False))
        page = self.paginate_queryset(issued_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(issued_books, many=True)
        return Response({
            "message": "Issued books retrieved successfully!",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)


class ReturnBookView(generics.GenericAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = ReturnBookSerializer
    permission_classes = [permissions.IsAuthenticated]

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
