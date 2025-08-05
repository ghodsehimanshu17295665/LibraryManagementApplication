import factory
from .models import Author, Category, Book


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")
    email = factory.Faker("email")
    birth_date = factory.Faker("date_of_birth")
    nationality = factory.Faker("country")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    publication_date = factory.Faker("date")
    quantity = factory.Faker("random_int", min=1, max=100)
    image = factory.django.ImageField(color="blue")
    author = factory.SubFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)
