from flask import Flask
from .extensions import db, jwt, ma

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Registering folders (Blueprints)
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app