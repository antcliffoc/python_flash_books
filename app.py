import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

#setting app.config
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book, User

@app.route("/")
def hello():
    return "hello world!"

# Example's of information flow with routes
@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_book_details():
    author=request.args.get('author')
    published=request.args.get('published')
    return "Author : {}, Published: {}".format(author,published)

@app.route("/getallusers")
def get_all_users():
    try:
        users=User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
        return(str(e))

@app.route("/get/user/<id_>")
def get_user_by_id(id_):
    try:
        user=User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return(str(e))

@app.route("/getallbooks")
def get_all_books():
    try:
        books=Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return(str(e))

@app.route("/get/book/<id_>")
def get_book_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))

@app.route("/add/book", methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
            book=Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return(str(e))
    return render_template("newbookform.html")

@app.route("/sign_up", methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            user=User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            return "a new user has been signed up. user email={}".format(user.email)
        except Exception as e:
            return(str(e))
    return render_template("newuserform.html")

if __name__ == '__main__':
    app.run()
