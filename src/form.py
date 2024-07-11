from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired, ValidationError
from src.models import User
class RegistrationForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(
        min=5, max= 50
    )], render_kw={'placeholder': 'name'})
    surname = StringField(validators=[InputRequired(), Length(
        min=5, max=100
    )], render_kw={'placeholder': 'surname'})
    email = EmailField(validators=[InputRequired(), Length(
        min=10, max=100
    )], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=10, max=100
    )], render_kw={'placeholder': 'password'})
    submit = SubmitField('Register')

    def validate_user(self, name, surname, email):
        existing_user_login = User.query.filter_by(name=name.data, surname=surname.data, email=email.data).first()
        if existing_user_login:
            raise ValidationError(
                "That login is already exists. Pleace choose a diffrent one."
            )
        
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=10, max=100
    )], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=10, max=100
    )], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')

    def validate_user(self, name, surname, email):
        existing_user_login = User.query.filter_by(name=name.data, surname=surname.data, email=email.data).first()
        if existing_user_login:
            raise ValidationError(
                'This login already existing'
            )
        
class TaskForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(
        min=5, max=50
    )], render_kw={'placeholder': 'Title'})
    content = StringField(validators=[InputRequired(), Length(
        min=10
    )], render_kw={'placeholder': 'Content'})
    submit = SubmitField('Add task')