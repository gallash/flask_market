from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    # For the automatic validation, the method name should be [validate_]+[field name]. Pass in the .data
    def validate_username(self, username_to_check):
        if User.query.filter_by(username=username_to_check.data).first():
            ValidationError("Username exists. Choose another one")

    def validate_email(self, email_to_check):
        if User.query.filter_by(username=email_to_check.data).first():
            ValidationError("Email address exists. Choose another one")

    # We can apply more than one validator at a time by encapsulating everything them in a []
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = EmailField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

        
class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')