from flask import Flask
from database import init_db
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)

db = init_db(app)


from routes.books import books_bp
from routes.members import members_bp
from routes.auth import auth_bp  

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(members_bp, url_prefix='/members')

@app.route('/')
def home():
    return "Welcome to the Library Management System API"
if __name__ == '__main__':
    app.run(debug=True)
