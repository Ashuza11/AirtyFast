from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.models import User
from app import db
from app.forms import VendorForm

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    users = User.query.all()
    form = VendorForm()
    return render_template(
        "dashboard.html", users=users, vendor_form=form, current_page="dashboard"
    )


@bp.route("/add_vendor", methods=["POST"])
@login_required
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
    return redirect(url_for("main.dashboard"))
