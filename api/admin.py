from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Author, Book, Category, Course, Fine, IssuedBook, Student


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "birth_date", "nationality")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "category",
        "title",
        "publication_date",
        "quantity",
        "image",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "year")


@admin.register(Student)
class StudentAdmin(UserAdmin):
    model = Student
    list_display = (
        "username",
        "email",
        "course",
        "enrollment_number",
        "phone_number",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "course")
    search_fields = ("username", "email", "enrollment_number", "phone_number")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "enrollment_number",
                    "phone_number",
                    "course",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "enrollment_number",
                    "phone_number",
                    "course",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "book",
        "issue_date",  # Change 'issue_book' to a valid field
        "due_date",
        "return_date",
        "is_returned",
    )



@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ("id", "issued_book", "amount", "date")
