from django.core.management.base import BaseCommand
from api.models import Category, Book


class Command(BaseCommand):
    help = "Initialize the database with default categories and sample."

    def handle(self, *args, **kwargs):
        # List of categories with names and descriptions
        categories = [
            {
                "name": "Fiction",
                "description": "A genre of books that contain fictional stories.",
            },
            {
                "name": "Science",
                "description": "Books covering various branches of science.",
            },
            {
                "name": "Technology",
                "description": "Books about technology advancements and trends.",
            },
            {
                "name": "Mathematics",
                "description": "Books covering various topics in mathematics.",
            },
            {
                "name": "Computer Science",
                "description": "Books covering computer science and related topics.",
            },
        ]

        # Initialize categories in the database
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"description": category_data["description"]},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Category "{category.name}" added successfully.'
                    )
                )

        # # Add some sample books related to Computer Science category
        # computer_science_category = Category.objects.get(name="Computer Science")
        # sample_books = [
        #     {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "quantity": 5},
        #     {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "quantity": 3},
        #     {"title": "Clean Code", "author": "Robert C. Martin", "quantity": 2},
        # ]

        # for book_data in sample_books:
        #     Book.objects.get_or_create(
        #         title=book_data["title"],
        #         author=book_data["author"],  # Assuming this is a string, you'll need to adjust it if using an Author model.
        #         category=computer_science_category,
        #         defaults={"quantity": book_data["quantity"]}
        #     )

        self.stdout.write(
            self.style.SUCCESS(
                "Database successfully initialized with default categories and sample."
            )
        )
