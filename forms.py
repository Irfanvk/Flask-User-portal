# from flask import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired
# from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField


class SignupForm(FlaskForm):
    """docstring for SignupForm"""
    first_name = StringField('First name', validators=[
                             DataRequired("please enter the first name")])
    last_name = StringField('Last name', validators=[
                            DataRequired("please enter the last name")])
    email = StringField('Email', validators=[DataRequired(
        "please enter the email address"), Email("please enter your email address")])
    password = PasswordField('Password', validators=[
                             DataRequired("Please enter a password"), Length(min=6, max=12, message="password must be atleast 6 characters")])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    """docstring for SignupForm"""
    email = StringField('Email', validators=[DataRequired(
        "please enter the email address"), Email("please enter your email address")])
    password = PasswordField('Password', validators=[
                             DataRequired("Please enter a password"), Length(min=6, max=12, message="password must be atleast 6 characters")])
    submit = SubmitField('Login')


class AddressForm(FlaskForm):
    """docstring for AddressForm"""
    address = StringField('Address', validators=[
                          DataRequired("Please enter an address")])
    submit = SubmitField('Search')
