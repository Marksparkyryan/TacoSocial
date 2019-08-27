from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import (DataRequired, Email, ValidationError, Length,
                                EqualTo)

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            email_exists,
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("password2", message="Passwords must match")
        ]
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
        ]
    )


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


class TacoForm(FlaskForm):
    protein = SelectField(
        "Protein",
        validators=[
            DataRequired()
        ],
        choices=[
            ("chicken", "chicken"),
            ("beef", "beef"),
            ("fish", "fish")
        ]
    )
    shell = SelectField(
        "Shell",
        validators=[
            DataRequired()
        ],
        choices=[
            ("corn", "corn"),
            ("flour", "flour")
        ]
    )
    cheese = SelectField(
        "Cheese",
        validators=[
            DataRequired()
        ],
        choices=[
            ("Yes please!", True),
            ("No thanks.", False)
        ]
    )
    extras = StringField(
        "Extras", 
    )
