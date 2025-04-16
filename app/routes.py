from flask import render_template, redirect, url_for, flash
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from app.forms import LoginForm, RegistrationForm  # Assuming you have these forms


# Main landing page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard (protected route)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# Login functionality
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Successfully logged in!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html", title="Sign In", form=form)


# Registration functionality
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists
        existing_user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


# Logout functionality
@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("home"))
