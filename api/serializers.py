from rest_framework import serializers
from django.contrib.auth import authenticate
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
    course = CourseSerializer(read_only=True)

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


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "username",
            "email",
            "password",
            "enrollment_number",
            "phone_number",
        ]

    def create(self, validated_data):
        student = Student.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            enrollment_number=validated_data["enrollment_number"],
            phone_number=validated_data["phone_number"],
        )
        student.set_password(validated_data["password"])
        student.save()
        return student


class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


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
