# Library Management System - Flask API

# Project Overview:
This project is a simple Library Management System built using Flask, with features for managing books and members. It supports CRUD (Create, Read, Update, Delete) operations for both books and members. Additionally, it provides optional pagination, search functionality, and token-based authentication (JWT) for added security.

How to Run the Project:
Clone the Repository: Clone this repository to your local machine.

bash
Copy code
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
Create and Activate Virtual Environment: It is recommended to use a virtual environment to manage dependencies.

bash
Copy code
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies: Install the required packages using pip.

bash
Copy code
pip install -r requirements.txt
Create the Database: Run the Flask application to automatically create the SQLite database (library.db).

bash
Copy code
python app.py
Access the API: The application will run locally on http://127.0.0.1:5000/. You can use a tool like Postman or cURL to interact with the API.

# Endpoints:

POST /auth/login: Login route to authenticate and generate JWT token.

GET /books: List all books.

POST /books: Add a new book.

PUT /books/<id>: Update an existing book.

DELETE /books/<id>: Delete a book.

GET /members: List all members.

POST /members: Add a new member.

PUT /members/<id>: Update an existing member.

DELETE /members/<id>: Delete a member.
For more details on the API, refer to the documentation below.

# Design Choices Made:
1. Flask Framework:

Chose Flask as the web framework due to its simplicity and flexibility, making it ideal for small projects like this Library Management System.

2. Database:

Used SQLite for the database. It is a lightweight, file-based database, which makes it easy to set up and use for small-scale applications. The models are defined using SQLAlchemy, which provides an easy-to-use ORM for interacting with the database.

3. JWT Authentication:

Implemented JWT (JSON Web Token) for token-based authentication. This was used to protect specific routes, requiring a valid JWT token to access protected resources like creating, updating, or deleting books and members.

4. Blueprints:

Used Blueprints to organize the code into modular sections. The app consists of three main blueprints: auth (for authentication), books (for book-related routes), and members (for member-related routes). This structure allows easy extension of the app if needed.

5. Error Handling:

Basic error handling is implemented, such as checking if a book or member exists before updating or deleting. If not found, a 404 error is returned. The POST methods check for missing required fields and return a 400 error.

6. Pagination:

Pagination is implemented for the /books and /members endpoints, which allows the user to retrieve a specific number of records per page.

7. Search:

Search functionality is added for books, allowing users to search books by title or author.

# Assumptions or Limitations:

1. Security:

For the sake of simplicity, the user data for JWT authentication is hardcoded (in auth.py). In a real application, user credentials should be stored securely in a database with hashed passwords.

2. Database:

The application uses a simple SQLite database. This may not be suitable for larger production systems. For production, a more robust database (like MySQL or PostgreSQL) could be used.

3. Testing:

Automated tests have not been implemented. This can be added using testing frameworks like pytest to ensure the correctness of the API.

4. Pagination Limits:

Pagination works with a fixed limit of 5 items per page. This can be customized by passing the page and per_page query parameters in the request.

5. Search Functionality:

The search functionality for books by title or author works by checking if the search term exists in the book's title or author field. This is a simple search, and more advanced search techniques (e.g., full-text search) could be implemented for better performance.

6. Assumed Environment:

The application assumes that you are using a local environment with Python 3.x and pip for package management.
