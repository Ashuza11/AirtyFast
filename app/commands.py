import click
from werkzeug.security import generate_password_hash
from flask import current_app
from app.models import User, db


def register_commands(app):
    @app.cli.command("init-admin")
    @click.option("--username", default="admin")
    @click.option("--email", default="admin@airtyfast.com")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def init_admin(username, email, password):
        """Initialize the admin user"""
        with app.app_context():
            if User.query.filter_by(email=email).first():
                click.echo("⚠️ Admin user already exists!")
                return

            try:
                admin = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role="superadmin",
                    is_active=True,
                )
                db.session.add(admin)
                db.session.commit()
                click.echo(f"✅ Admin '{username}' created successfully!")
                click.echo(f"   Email: {email}")
            except Exception as e:
                db.session.rollback()
                click.echo(f"❌ Error creating admin: {str(e)}", err=True)
