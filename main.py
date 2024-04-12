from flask  import request, jsonify
from config import app, db
from model import Book
from flask import Flask, request, jsonify, send_file
import json

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

@app.route('/books/getbook/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_json())



ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/books', methods=['POST'])
def create_book():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        app.logger.info(f'Saving file {filename} to {app.config["UPLOAD_FOLDER"]}')

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        jsonData = request.form.get('requestData')
        requestData = json.loads(jsonData)

        requestData = json.loads(jsonData)
        title = requestData.get('title')

        if not title:
            return jsonify({'error': 'Please provide title'}), 400

        # Save title, filename to the database
        new_book = Book(title=title, fileName=filename)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book uploaded successfully', 'book': new_book.to_json()}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    

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


@app.route('/books/getbookpdf/<int:book_id>', methods=['GET'])
def fetch_book(book_id):
    # Assuming book_id is present in the book database
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    fileName = book.fileName  # Assuming your Book model has a fileName attribute
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], fileName)

    if os.path.exists(file_path):
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Book file not found"}), 404
        
        


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)