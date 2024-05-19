from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()


def create_app() :
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steam_recap.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    
    swagger = Swagger(app)

    from .blueprints.user import user_bp
    from .blueprints.genre import genre_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(genre_bp, url_prefix='/api')

    with app.app_context():
        from .models.user import User
        db.create_all()

    return app

