from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try to log in or enter a different username.')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already linked to account! Please try to log in or enter a different email.')

    username = StringField(label='Username:', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=7), DataRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Submit!')


class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit!')


class BuyItemForm(FlaskForm):
    submit = SubmitField(label='Buy game')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell game')
