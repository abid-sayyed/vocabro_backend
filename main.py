from flask  import request, jsonify
from config import app, db
from model import Book
from flask import Flask, request, jsonify

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


@app.route('/')
def home():
    return jsonify({'message': 'Hello, World!'})


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_json = [book.to_json() for book in books]
    return jsonify(books_json)



ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/books', methods=['POST'])
def create_book():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
    data = request.json
    if 'title' not in data or 'fileName' not in data:
        return jsonify({'error': 'Please provide title and fileName'}), 400
    book = Book(title=data['title'], fileName=data['fileName'])
    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify(book.to_json(), "Book created successfully")




@app.route('/books/<int:id>', methods=['PATCH'])    
def update_book(id):
    data = request.json
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    if 'title' in data:
        book.title = data['title']
    if 'fileName' in data:
        book.fileName = data['fileName']
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(book.to_json(), "Book updated successfully")

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify("Book deleted successfully"), 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)