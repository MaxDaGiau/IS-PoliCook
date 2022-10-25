from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, Label
from wtforms.validators import DataRequired

from models import *

homepage_blueprint = Blueprint("homepage_bp", __name__)

db = SQLAlchemy()

class PostForm(FlaskForm):
    text_area = TextAreaField("Text area", validators=[DataRequired()])
    post_picture = FileField("Image File")
    image_loader_label = Label(field_id="image-loader", text="")
    submit = SubmitField("Publish")


@homepage_blueprint.route("/", methods=["GET", "POST"])
@login_required
def homepage():

    friends_ids = [friend.id for friend in current_user.friends]
    
    all_posts = FeedPost.query.filter(FeedPost.user_id.in_(friends_ids + [current_user.id])).all()
    all_comments = RecipeVariation.query.filter(RecipeVariation.user_id.in_(friends_ids)).all()

    posts = [{"user": User.query.filter_by(id=p.user_id).first(), "post": p} for p in all_posts]
    comments = [{
        "user": User.query.filter_by(id=c.user_id).first(),
        "comment": c,
        "recipe": Recipe.query.filter_by(id=c.recipe_id).first()} for c in all_comments]
    
    
    post_form = PostForm()

    if post_form.validate_on_submit():
        
        post_text = post_form.text_area.data

        if 'post_picture' in post_form:
            file = post_form.post_picture.data
            picture = file.read()
            rendered_picture = base64.b64encode(picture).decode('ascii')

            feed_post = FeedPost(
                user_id=current_user.id,                
                text=post_text,
                picture=picture,
                rendered_picture=rendered_picture
            )

        else:
            feed_post = FeedPost(
                user_id=current_user.id,
                text=post_text
            )

        db.session.add(feed_post)
        db.session.commit()

        return redirect(url_for('homepage_bp.homepage'))

    else:
        return render_template('homepage.html', current_user=current_user, posts=posts, comments=comments, form=post_form)

            