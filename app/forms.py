from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Vendor ID",
        validators=[DataRequired()],
        render_kw={"placeholder": "Your business ID"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Access Dashboard")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if not user:
            raise ValidationError("This vendor ID is not registered")

    def validate_password(self, password):
        user = db.session.scalar(
            sa.select(User).where(User.username == self.username.data)
        )
        if user and not user.check_password(password.data):
            raise ValidationError("Incorrect password")


# class RegistrationForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     password2 = PasswordField(
#         "Repeat Password", validators=[DataRequired(), EqualTo("password")]
#     )
#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         user = db.session.scalar(sa.select(User).where(User.username == username.data))
#         if user is not None:
#             raise ValidationError("Please use a different username.")

#     def validate_email(self, email):
#         user = db.session.scalar(sa.select(User).where(User.email == email.data))
#         if user is not None:
#             raise ValidationError("Please use a different email address.")
