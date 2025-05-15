from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# Extensions initialization (no app-bound yet)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "login"


def create_app(config_class=Config):
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = "auth.login"

    # Register blueprints
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    # Register commands
    from app.commands import register_commands

    register_commands(app)

    # Initialize admin user in development
    with app.app_context():
        from app.models import User

        db.create_all()  # Create tables if they don't exist

        # Create admin if no users exist (DEV ONLY)
        if app.config.get("FLASK_ENV") == "development" and User.query.count() == 0:
            admin = User(
                username="admin",
                email="admin@airtyfast.com",
                password_hash=generate_password_hash("cat123"),
                role="superadmin",
                is_active=True,
            )
            db.session.add(admin)
            db.session.commit()
            print("Initial admin user created!")

    # Import and register error handlers
    from app import routes, models, errors

    return app
