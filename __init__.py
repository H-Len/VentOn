from flask_login import login_user
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if isinstance(DATABASE_URL, str):
            DATABASE_URL.replace('postgres://', 'postgresql://')
        else:
            DATABASE_URL = 'postgresql://localhost:5432/database'
            
    except KeyError as err:
        DATABASE_URL = 'postgresql://localhost:5432/database'
    app.config['SECRET_KEY'] = 'k3n%L$knn(9()wl_-o'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Author

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Author.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
