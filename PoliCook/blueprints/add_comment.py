from flask_login import current_user, login_required
from flask import Blueprint, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Recipe, RecipeVariation, User
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, Label
from wtforms.validators import DataRequired
from sqlalchemy import asc
import base64

db = SQLAlchemy(session_options={"autoflush": False})

add_comment_blueprint = Blueprint("add_comment_bp", __name__, static_folder="static")

class CommentForm(FlaskForm):
    text_area = TextAreaField("Text area", validators=[DataRequired()])
    comment_picture = FileField("Image File")
    image_loader_label = Label(field_id="image-loader", text="")
    submit = SubmitField("Publish")

@add_comment_blueprint.route('/add_comment/<recipe_id>', methods=['POST', 'GET'])
@login_required
def add_comment(recipe_id):
  
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        abort(404)

    friends_ids = [friend.id for friend in current_user.friends]
        
    comments = RecipeVariation.query.filter_by(recipe_id=recipe.id).order_by(asc(RecipeVariation.creation_time)).all()
    comments = [c for c in comments if c.user_id in friends_ids or c.user_id == current_user.id]

    comments_with_profile_pictures = []
    
    for c in comments:
        user = User.query.filter_by(id=c.user_id).first()
        comments_with_profile_pictures.append({
            "comment": c,
            "user": user
            })

    comment_form = CommentForm()

    if comment_form.validate_on_submit():

        text_comment = comment_form.text_area.data

        if 'comment_picture' in comment_form:
            file = comment_form.comment_picture.data
            picture = file.read()
            rendered_picture = base64.b64encode(picture).decode('ascii')

            recipe_variation = RecipeVariation(
                user_id=current_user.id,
                recipe_id=recipe.id,
                text = text_comment,
                picture=picture,
                rendered_picture=rendered_picture)
        else:
            recipe_variation = RecipeVariation(
                user_id=current_user.id,
                recipe_id=recipe.id,
                text = text_comment)
        
        db.session.add(recipe_variation)
        db.session.commit()

        friends_ids = [friend.id for friend in current_user.friends]
        
        comments = RecipeVariation.query.filter_by(recipe_id=recipe.id).order_by(asc(RecipeVariation.creation_time)).all()
        comments = [c for c in comments if c.user_id in friends_ids or c.user_id == current_user.id]

        comments_with_profile_pictures = []
        
        for c in comments:
            user = User.query.filter_by(id=c.user_id).first()
            comments_with_profile_pictures.append({
                "comment": c,
                "user": user
                })
        return redirect(url_for('add_comment_bp.add_comment', recipe_id=recipe_id))

    return render_template("recipe.html", user=current_user, recipe=recipe, comments=comments_with_profile_pictures, form=comment_form)
