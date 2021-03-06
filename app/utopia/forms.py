from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from utopia.user_service import UserService



class RegistrationForm(FlaskForm):

    given_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    family_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


