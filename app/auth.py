from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app.models import User
from app import db
from app.forms import LoginForm, ForgotPasswordForm

# Create a Blueprint named 'auth'
bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("auth.login"))  # Updated to use blueprint name
        login_user(user, remember=form.remember_me.data)
        flash("Successfully logged in!", "success")
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.dashboard")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user:
            flash(
                "Password reset instructions sent to your registered email", "success"
            )
            return redirect(url_for("auth.login"))
        flash("Vendor ID not found", "danger")

    return render_template("forgot_password.html", form=form)
