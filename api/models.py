import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Author(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="book_pics/", blank=True, null=True)

    def __str__(self):
        return self.title


class Course(TimeStampedModel):
    YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
        (4, "4th Year"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField(choices=YEAR_CHOICES)

    def __str__(self):
        return self.name


class Student(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.SET_NULL
    )
    enrollment_number = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.enrollment_number})"

    class Meta:
        verbose_name = "Students name"
        verbose_name_plural = "Students name"


class IssuedBook(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.student.username}"


class Fine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued_book = models.ForeignKey(IssuedBook, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Fine of {self.amount} for {self.issued_book.book.title}"
