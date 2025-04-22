from flask import render_template, redirect, url_for, flash, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
import sqlalchemy as sa
from urllib.parse import urlsplit
from app.models import User

from app.forms import LoginForm, RegistrationForm, ForgotPasswordForm, VendorForm


# Main landing page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard (protected route)
@app.route("/dashboard")
@login_required
def dashboard():
    users = [
        {
            "name": "N/A",
            "email": "admin@example.com",
            "role": "Superuser",
            "active": True,
            "is_current": True,
        },
        {
            "name": "User",
            "email": "user@example.com",
            "role": "User",
            "active": True,
            "is_current": False,
        },
        {
            "name": "User2",
            "email": "user2@example.com",
            "role": "User",
            "active": False,
            "is_current": False,
        },
    ]
    users = User.query.all()
    form = VendorForm()
    return render_template(
        "dashboard.html", users=users, vendor_form=form, current_page="user_setting"
    )


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
        # flash("Successfully logged in!", "success")
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("dashboard")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


# Logout functionality
@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if user:
            # Add password reset logic here
            flash(
                "Password reset instructions sent to your registered email", "success"
            )
            return redirect(url_for("login"))

        flash("Vendor ID not found", "danger")

    return render_template("forgot_password.html", form=form)


# add vendor
@app.route("/add_vendor", methods=["POST"])
def add_vendor():
    form = VendorForm()
    if form.validate_on_submit():
        vendor = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data),
            role="vendor",
            is_active=form.is_active.data,
        )
        db.session.add(vendor)
        db.session.commit()
        flash("Vendor added successfully!", "success")
    else:
        flash("Failed to add vendor. Check inputs.", "danger")
    return redirect(url_for("dashboard"))
