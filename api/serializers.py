import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Author, Book, Category, Course, Fine, IssuedBook, Student
from datetime import datetime, timedelta


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "email", "birth_date", "nationality"]

    # def validate(self, data):
    #     name = data.get('name')
    #     nationality = data.get('nationality')

    #     if name and not name.isalpha():
    #         raise serializers.ValidationError({"name": "The name field must only contain alphabetic characters."})

    #     if nationality and not nationality.isalpha():
    #         raise serializers.ValidationError({"nationality": "The nationality field must only contain alphabetic characters."})

    #     return data
    def validate(self, data):
        name = data.get('name')
        nationality = data.get('nationality')

        # Allow alphabetic characters and spaces using regex
        name_pattern = r'^[a-zA-Z\s]+$'
        nationality_pattern = r'^[a-zA-Z\s]+$'

        if name and not re.match(name_pattern, name):
            raise serializers.ValidationError({"name": "The name field must only contain alphabetic characters and spaces."})

        if nationality and not re.match(nationality_pattern, nationality):
            raise serializers.ValidationError({"nationality": "The nationality field must only contain alphabetic characters and spaces."})

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    def validate(self, data):
        name = data.get('name')
        description = data.get('description')

        # Allow alphabetic characters and spaces using regex
        name_pattern = r'^[a-zA-Z\s]+$'
        if name and not re.match(name_pattern, name):
            raise serializers.ValidationError({"name": "The name field must only contain alphabetic characters and spaces."})

        description_pattern = r'^[a-zA-Z0-9\s.,!?]+$'
        if description and len(description) < 10:
            raise serializers.ValidationError({"description": "The description must be at least 10 characters long."})
        if description and not re.match(description_pattern, description):
            raise serializers.ValidationError({"description": "The description can only contain letters, numbers, spaces, and specific punctuation."})

        return data

    def create(self, validated_data):
        # Check if a category with the same name already exists
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({"name": "A category with this name already exists."})

        # If the category does not exist, create a new one
        return super().create(validated_data)


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='email', queryset=Author.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

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

    def validate_title(self, value):
        # Validate that the title is not empty and has a minimum length of 3 characters
        if not value or len(value) < 3:
            raise serializers.ValidationError("The title must be at least 3 characters long.")

        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("The title must contain at least one alphabetic character.")

        return value

    def create(self, validated_data):
        # Check if a category with the same name already exists
        if Book.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError({"title": "A Book already exists."})

        # If the category does not exist, create a new one
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "description", "year"]

    def validate(self, data):
        name = data.get('name')
        description = data.get('description')

        # Allow alphabetic characters and spaces using regex
        name_pattern = r'^[a-zA-Z\s]+$'
        if name and not re.match(name_pattern, name):
            raise serializers.ValidationError({"name": "The name field must only contain alphabetic characters and spaces."})

        description_pattern = r'^[a-zA-Z0-9\s.,!?]+$'
        if description and len(description) < 10:
            raise serializers.ValidationError({"description": "The description must be at least 10 characters long."})
        if description and not re.match(description_pattern, description):
            raise serializers.ValidationError({"description": "The description can only contain letters, numbers, spaces, and specific punctuation."})

        return data

    def create(self, validated_data):
        name = validated_data['name']
        year = validated_data['year']

        # Check if a course with the same name and year exists
        if Course.objects.filter(name=name, year=year).exists():
            raise serializers.ValidationError({"name": "A course with this name and year already exists."})

        # If the course does not exist or the year is different, create a new one
        return super().create(validated_data)


class StudentSerializer(serializers.ModelSerializer):
    # Allow course to be updated by its name
    course = serializers.SlugRelatedField(
        slug_field="name",  # Use course name for updates
        #  Ensure the queryset contains all courses
        queryset=Course.objects.all(),
    )

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
    course = serializers.SlugRelatedField(
        slug_field="name",  # Allows using course name instead of course ID
        # You need to provide a queryset to look up the Course by name
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Student
        fields = [
            "username",
            "email",
            "password",
            "course",  # The course name will be provided here
            "enrollment_number",
            "phone_number",
        ]

    def validate_phone_number(self, value):
        # Validate that phone number is not empty and 10 digits
        if not value or not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("The phone number must be exactly 10 digits.")
        return value

    def create(self, validated_data):
        student = Student.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            # Course object is automatically looked up by name
            course=validated_data["course"],
            enrollment_number=validated_data["enrollment_number"],
            phone_number=validated_data["phone_number"],
        )
        student.set_password(validated_data["password"])
        student.save()

        return student


class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class IssuedBookSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
        read_only_fields = [
            "issue_date",
            "due_date",
            "return_date",
            "is_returned",
        ]

    def validate(self, data):
        book = data.get("book")
        student = self.context["request"].user

        # Check if the book exists and is available
        if book.quantity <= 0:
            raise serializers.ValidationError("No Book available to issue")

        # Check if the book is already issued and not returned by the student
        is_book_issued = IssuedBook.objects.filter(
            book=book, student=student, is_returned=False
        ).exists()
        if is_book_issued:
            raise serializers.ValidationError(
                "Book is already issued and not returned"
            )

        return data

    def create(self, validated_data):
        book = validated_data["book"]
        student = validated_data["student"]

        # Decrease the book quantity
        book.quantity -= 1
        book.save()

        # Automatically set issue and due dates
        issued_book = IssuedBook.objects.create(
            book=book,
            student=student,
            issue_date=datetime.now().date(),
            due_date=datetime.now().date() + timedelta(days=10),
            is_returned=False,
        )

        return issued_book


class ReturnBookSerializer(serializers.Serializer):
    # issued_book = serializers.IntegerField()
    issued_book = serializers.UUIDField(
        format="hex_verbose"
    )  # Expecting a UUID

    def validate(self, data):
        issued_book_id = data.get("issued_book")

        # Check if the issued book exist
        issued_book = IssuedBook.objects.filter(id=issued_book_id).first()
        if not issued_book:
            raise serializers.ValidationError(
                {"msg": "Issued book record not found."}
            )

        # Check if the book has already been returned
        if issued_book.is_returned:
            raise serializers.ValidationError(
                {"msg": "This book has already been returned."}
            )

        # Save the issued book instance in the validated data
        data["issued_book_instance"] = issued_book
        return data

    def save(self, student):
        # Retrieve the issued book instance from validated data
        issued_book = self.validated_data["issued_book_instance"]

        # Check if the student is authenticated
        if not student.is_authenticated:
            raise serializers.ValidationError(
                {"msg": "User not authenticated"}
            )

        # Mark the book as returned
        issued_book.is_returned = True
        issued_book.return_date = datetime.now().date()
        issued_book.save()

        # Get the associated book and increase the quantity
        book = issued_book.book
        book.quantity += 1
        book.save()

        return issued_book


class FineSerializer(serializers.ModelSerializer):
    issued_book = IssuedBookSerializer()

    class Meta:
        model = Fine
        fields = ["id", "issued_book", "amount", "date"]
