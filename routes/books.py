from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError  # Import for catching IntegrityError
from database import db
from models import Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn']
    )
    
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully', 'id': new_book.id}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Book with the same ISBN already exists!"}), 400

# GET /books/
@books_bp.route('/', methods=['GET'])
def get_books():
    search_title = request.args.get('title')
    search_author = request.args.get('author')
    
    query = Book.query
    
    if search_title:
        query = query.filter(Book.title.ilike(f"%{search_title}%"))
    
    if search_author:
        query = query.filter(Book.author.ilike(f"%{search_author}%"))
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'current_page': books.page,
        'items': [{'id': book.id, 'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books.items],
        'pages': books.pages,
        'per_page': per_page,
        'total': books.total
    })


# POST /books/add-sample
@books_bp.route('/add-sample', methods=['POST'])
def add_sample_books():
    Book.query.delete()
    db.session.commit()

    sample_books = [
        {"title": "Book 1", "author": "Author 1", "isbn": "1234567890"},
        {"title": "Book 2", "author": "Author 2", "isbn": "1234567891"},
        {"title": "Book 3", "author": "Author 3", "isbn": "1234567892"},
    ]
    
    # Adding books to the session
    for book in sample_books:
        new_book = Book(title=book['title'], author=book['author'], isbn=book['isbn'])
        db.session.add(new_book)
    
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "One or more books could not be added due to duplicate ISBNs."}), 400
    
    return jsonify({"message": "Sample books added successfully!"}), 201


# PUT /books/<book_id>
@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update book due to integrity error."}), 400
    
    return jsonify({'message': 'Book updated successfully'})


# DELETE /books/<book_id>
@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Book deleted successfully'})


# GET /books/search
@books_bp.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q')
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) | (Book.author.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books])
