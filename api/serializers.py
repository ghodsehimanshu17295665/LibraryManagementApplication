from rest_framework import serializers

from .models import Author, Book, Category, Course, Fine, IssuedBook, Student


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "email", "birth_date", "nationality"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "category",
            "title",
            "publication_date",
            "quantity",
            "image",
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "description", "year"]


class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "email",
            "course",
            "enrollment_number",
            "phone_number",
        ]


class IssuedBookSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    book = BookSerializer()

    class Meta:
        model = IssuedBook
        fields = [
            "id",
            "student",
            "book",
            "issue_date",
            "due_date",
            "return_date",
            "is_returned",
        ]


class FineSerializer(serializers.ModelSerializer):
    issued_book = IssuedBookSerializer()

    class Meta:
        model = Fine
        fields = ["id", "issued_book", "amount", "date"]
