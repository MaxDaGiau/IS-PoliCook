from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from settings import *

db = SQLAlchemy(session_options={"autoflush": False})

ingredients = db.Table('ingredients',
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

friendship = db.Table('friendships', 
    db.Column('a_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('b_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key =True)
    dish_type = db.Column(db.String(100))
    name = db.Column(db.String(100))
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
        backref=db.backref('recipes', lazy=True))
    instructions = db.Column(db.Text())
    picture = db.Column(db.LargeBinary, nullable=True) # Actual data, needed for Download
    rendered_picture = db.Column(db.Text, nullable=True) # Data to render the pic in browser

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100), nullable = False, unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    course_of_study = db.Column(db.String(100))
    profile_picture = db.Column(db.LargeBinary, nullable=True) # Actual data, needed for Download
    rendered_profile_picture = db.Column(db.Text, default=DEFAULT_PROFILE_PICTURE) # Data to render the pic in browser
    password = db.Column(db.String(100))
    id_for_friendship = db.Column(db.String(10), unique=True)
    friends = db.relationship('User',
            secondary=friendship,
            primaryjoin=id==friendship.c.a_id,
            secondaryjoin=id==friendship.c.b_id,
            lazy='dynamic')



class RecipeVariation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    text = db.Column(db.Text())
    picture = db.Column(db.LargeBinary, nullable=True) # Actual data, needed for Download
    rendered_picture = db.Column(db.Text, nullable=True) # Data to render the pic in browser
    creation_time = db.Column(db.DateTime, default=datetime.now)

class FeedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text())
    picture = db.Column(db.LargeBinary, nullable=True) # Actual data, needed for Download
    rendered_picture = db.Column(db.Text, nullable=True) # Data to render the pic in browser
    creation_time = db.Column(db.DateTime, default=datetime.now)
    