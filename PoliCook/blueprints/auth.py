from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired
from models import User
from cds import TRIENNALI, MAGISTRALI
import base64, secrets

db = SQLAlchemy()
auth_blueprint = Blueprint('auth', __name__)

# Custom validator - l'ho scritto io
# Devono per forza prendere come parametri form e field
# check if the user actually exists
# take the user-supplied password, hash it, and compare it to the hashed password in the database
def validate_user(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    # se l'utente esiste, non è None
    if not user or not check_password_hash(user.password, form.password.data):
        raise ValidationError("Please check your login details and try again.")


class LoginForm(FlaskForm):    
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), validate_user])
    remember_me = BooleanField()
    submit = SubmitField('Login')
    

# Controlla che sia polito e che la mail dell'utente non esista già
def validate_email(form, field):
    email = field.data
    email_domain = email.split("@")[1]
    if email_domain != "studenti.polito.it":
        raise ValidationError('The access is restricted to politecnico students, please use your university mail (studenti.polito.it)')
    
    user = User.query.filter_by(email=email).first()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        raise ValidationError('Email address already exists')

# Controlla che il nome non contenga numeri
def validate_name(form, field):
    name = field.data
    for char in name:
        if char.isdigit():
            raise ValidationError("First name and last name cannot contain numbers")
            
class SignupForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), validate_name])
    last_name = StringField("Last name", validators=[DataRequired(), validate_name])
    email = EmailField("Email", validators=[DataRequired(), validate_email])
    password = PasswordField("Password", validators=[DataRequired()])
    course_of_study = SelectField('Course of study', choices=TRIENNALI + MAGISTRALI)
    submit = SubmitField('Signup')


@auth_blueprint.route('/login', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('homepage_bp.homepage'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
    
        email = login_form.email.data
        remember = login_form.remember_me.data

        user = User.query.filter_by(email=email).first()

        login_user(user, remember=remember)
        return redirect(url_for('homepage_bp.homepage'))
    else:
        return render_template('login.html', form=login_form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    
    signup_form = SignupForm()
    
    if signup_form.validate_on_submit():
        first_name = signup_form.first_name.data
        surname = signup_form.last_name.data
        course_of_study = signup_form.course_of_study.data
        email = signup_form.email.data
        password = signup_form.password.data
        password_hash = generate_password_hash(password, method='sha256')

        new_user = User(
            name=first_name,
            surname=surname,
            email=email,
            password=password_hash,
            id_for_friendship = secrets.token_urlsafe(10),
            course_of_study=course_of_study
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
    
        return redirect(url_for('homepage_bp.homepage'))
    else:
        return render_template('signup.html', form=signup_form)
        

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully", "message")
    return redirect(url_for('auth.login'))