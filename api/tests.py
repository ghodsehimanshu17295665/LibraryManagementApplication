import uuid
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import AuthorFactory, CategoryFactory, BookFactory
# from .models import Author, Category, Book


class AuthorViewTests(APITestCase):

    def setUp(self):
        # Get the custom user model
        User = get_user_model()

        # Create a superuser using the custom user model
        self.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="password123",
        )

        # Ensure the superuser is created
        self.assertTrue(
            self.superuser.is_superuser, "Superuser creation failed"
        )
        self.assertTrue(self.superuser.is_staff, "Superuser should be staff")

        # Generate JWT token for the superuser
        refresh = RefreshToken.for_user(self.superuser)
        self.token = str(
            refresh.access_token
        )  # This is the token you will use for authentication

        # Create a sample author using Factory Boy
        self.author = AuthorFactory.create()  # Create a random author
        self.url_list = reverse(
            "author-list-create"
        )  # URL for creating authors
        self.url_detail = reverse(
            "author-detail", kwargs={"pk": self.author.id}
        )  # URL for author details

    def test_get_author_list(self):
        """Test the GET method for retrieving a list of authors."""
        # Include the JWT token in the request header
        response = self.client.get(
            self.url_list, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Only one author should be in the DB

    def test_get_author_detail(self):
        """Test the GET method for retrieving a single author."""
        # Include the JWT token in the request header
        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.author.name)
        self.assertEqual(response.data["email"], self.author.email)

    def test_post_create_author(self):
        """Test the POST method to create a new author."""
        data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "birth_date": "1992-05-15",
            "nationality": "British",
        }

        # Send POST request to create a new author, with the JWT token in the Authorization header
        response = self.client.post(
            self.url_list,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        # Assert that the response status is HTTP 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(
            response.data["message"], "Author created successfully!"
        )
        self.assertEqual(response.data["author"]["name"], data["name"])

    def test_put_update_author(self):
        """Test the PUT method to update an existing author."""
        updated_data = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "birth_date": "1992-01-01",
            "nationality": "Canadian",
        }

        # Send PUT request to update the author, with the JWT token in the Authorization header
        response = self.client.put(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        # Assert that the response status is HTTP 200 (OK) since the author should be updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content to ensure the author was updated
        self.assertEqual(response.data["author"]["name"], updated_data["name"])
        self.assertEqual(
            response.data["author"]["email"], updated_data["email"]
        )

    def test_patch_update_author(self):
        """Test the PATCH method to partial update an existing author."""
        updated_data = {"nationality": "Indian"}

        # Send PATCH request to partially update the author, with the JWT token in the Authorization header
        response = self.client.patch(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        # Assert that the response status is HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # nationality field is updated
        self.assertEqual(
            response.data["author"]["nationality"], updated_data["nationality"]
        )

    def test_delete_author(self):
        """Test the DELETE method to delete an existing author."""
        # send DELETE request to delete the author, with the JWT token in the Authorization header
        response = self.client.delete(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the author no longer exists by trying to get the author's details
        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_author_invalid_data(self):
        """Test the POST method with invalid data."""
        invalid_data = {
            "name": "",
            "email": "abc",
            "birth_date": "1992-01-0101",
            "nationality": "British",
        }

        # Send POST request with invalid data
        response = self.client.post(
            self.url_list,
            invalid_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        # Assert that the response status is HTTP 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that the correct validation errors are present in the response data
        self.assertIn("name", response.data)
        self.assertIn("email", response.data)
        self.assertIn("birth_date", response.data)

    def test_get_author_not_found(self):
        """Test the GET method when trying to retrieve an author that doesn't exist."""
        # Generate a random UUID for a non-existent author
        non_existent_pk = uuid.uuid4()

        # URL for a non-existent author
        non_existent_url = reverse(
            "author-detail", kwargs={"pk": non_existent_pk}
        )

        # Send GET request for a non-existent author
        response = self.client.get(
            non_existent_url, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        # Assert that the response status is HTTP 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="password123",
        )
        refresh = RefreshToken.for_user(self.superuser)
        self.token = str(refresh.access_token)

        self.category = CategoryFactory.create()
        self.url_list = reverse("categories-list-create")
        self.url_detail = reverse(
            "categories-detail", kwargs={"pk": self.category.id}
        )

    def test_get_category_list(self):
        response = self.client.get(
            self.url_list, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category_detail(self):
        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_post_create_category(self):
        data = {"name": "Science"}
        response = self.client.post(
            self.url_list,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["category"]["name"], data["name"])

    def test_put_update_category(self):
        updated_data = {"name": "Computer Science"}
        response = self.client.put(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["category"]["name"], updated_data["name"]
        )

    def test_patch_update_category(self):
        updated_data = {"name": "Mechanical"}
        response = self.client.patch(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["category"]["name"], updated_data["name"]
        )

    def test_delete_category(self):
        response = self.client.delete(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="password123",
        )
        refresh = RefreshToken.for_user(self.superuser)
        self.token = str(refresh.access_token)

        self.book = BookFactory.create()
        self.url_list = reverse("books-list-create")
        self.url_detail = reverse("books-detail", kwargs={"pk": self.book.id})

    def test_get_book_list(self):
        response = self.client.get(
            self.url_list, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_book_detail(self):
        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_post_create_book(self):
        # Create related instances
        category = CategoryFactory.create()
        author = AuthorFactory.create()

        data = {
            "title": "Code",
            "publication_date": "2024-01-01",
            "quantity": 10,
            "author": author.email,
            "category": category.name,
        }
        response = self.client.post(
            self.url_list,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        # Assert response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"]["title"], data["title"])

    def test_put_update_book(self):
        updated_data = {
            "title": "Clean code",
            "publication_date": "2024-01-01",
            "quantity": 20,
            "author": self.book.author.email,
            "category": self.book.category.name,
        }

        response = self.client.put(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["title"], updated_data["title"])

    def test_patch_update_book(self):
        updated_data = {"title": "New Clean Code"}
        response = self.client.patch(
            self.url_detail,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["title"], updated_data["title"])

    def test_delete_book(self):
        response = self.client.delete(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            self.url_detail, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
