<!-- # LibraryManagementApplication

## TimeStampModel 

- **createdat** : Store current time of initial input data.

- **updatedat** : Store current time when user update the already stored data.

## AuthorModel 
 -->

# Library Management System

This project is a Library Management System built with Django. It handles the creation of books, authors, categories, students, and the management of book issuance, course enrollments, and fines for overdue returns.

## Features

- **User Authentication:** Custom user model for students, extending `AbstractUser`.
- **Book Management:** Add and categorize books by author and category.
- **Issuance System:** Issue books to students with return tracking and due dates.
- **Fine Calculation:** Calculate and track fines for late returns.
- **Course Enrollment:** Assign students to courses.

## Models Overview

1. **TimeStampedModel (Abstract Model):**
   - Provides `created_at` and `updated_at` fields for tracking when instances are created and updated.

2. **Author:**
   - Fields: `name`, `email`, `birth_date`, `nationality`.
   - Unique email for authors to avoid duplicates.

3. **Category:**
   - Fields: `name`, `description`.
   - Used to categorize books.

4. **Book:**
   - Fields: `author`, `category`, `title`, `publication_date`, `quantity`, `image`.
   - Relation with `Author` and `Category`.

5. **Course:**
   - Fields: `name`, `description`, `year`.
   - Year is chosen from predefined options (1st to 4th year).

6. **Student (Custom User Model):**
   - Fields: `course`, `enrollment_number`, `phone_number`.
   - Extends Django's `AbstractUser` for authentication and adds fields related to student information.

7. **IssuedBook:**
   - Tracks which books are issued to which students.
   - Fields: `student`, `book`, `issue_date`, `due_date`, `return_date`, `is_returned`.

8. **Fine:**
   - Linked to `IssuedBook`.
   - Fields: `issued_book`, `amount`, `date`.

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Djangorestframework 3.0+
- PostgreSQL (or any other supported database)


## Usage

- Admin panel: `http://localhost:8000/admin/`
- Add new authors, categories, books, and students through the admin interface.
- Issue books to students and track due dates, returns, and fines.

## Project Structure

- **models.py**: Contains all models related to books, authors, students, issuance, and fines.
- **managers.py**: Contains custom managers for the `Student` model.
- **admin.py**: Django admin configurations for managing models.
- **views.py**: Handles the logic for issuing books, handling fines, and other operations.

## Models in Detail

### 1. `Author`
   - Manages author details with a unique email for identification.
   
### 2. `Category`
   - Manages categories for classifying books.

### 3. `Book`
   - Contains information about each book, including author, category, and quantity.
   
### 4. `Student`
   - Custom user model extending Django’s `AbstractUser`, with additional fields like enrollment number, phone number, and course assignment.

### 5. `IssuedBook`
   - Tracks which book is issued to which student, with details about due dates and return status.

### 6. `Fine`
   - Tracks fines issued for late return of books.
