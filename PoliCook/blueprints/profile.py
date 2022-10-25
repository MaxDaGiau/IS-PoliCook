from flask import Blueprint, flash, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Label, FileField
from wtforms.validators import ValidationError, DataRequired
from flask_login import login_required, current_user
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import User
import base64

db = SQLAlchemy()

profile_blueprint = Blueprint("profile_bp", __name__)

def validate_id(form, field):
    if len(field.data) != 14:
        raise ValidationError("The ID to add a friend must be a 14 characters long ID!")

    friend = db.session.query(User).filter_by(id_for_friendship=field.data).first()

    if friend is None:
        raise ValidationError("This ID does not correspond to any user, check again or ask your friend to send it back")
    
    if friend.id == current_user.id:
        raise ValidationError("You can't add yourself as a friend")

class AddFriend(FlaskForm):
    id_for_friendship = StringField("Id for friendship", validators=[DataRequired(), validate_id])
    submit = SubmitField("Search")

class ChangeProfilePictureForm(FlaskForm):
    change_propic = Label(field_id="image", text="")
    image = FileField("Image file")
    

@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    my_friends = list(User.query.filter_by(id=current_user.id).first().friends)

    change_profile_picture_form = ChangeProfilePictureForm()
    add_friend_form = AddFriend()

    if change_profile_picture_form.image.data and change_profile_picture_form.validate_on_submit():
        change_profile_picture(change_profile_picture_form)

    if add_friend_form.submit.data and add_friend_form.validate_on_submit():
        add_friend(add_friend_form)

    return render_template('profile.html', user=current_user, friends=my_friends, add_friend_form=add_friend_form, change_form=change_profile_picture_form)

def change_profile_picture(form):
    file = form.image.data
    new_profile_picture = file.read()
    new_rendered_profile_picture = base64.b64encode(new_profile_picture).decode('ascii')

    user = db.session.query(User).filter_by(id=current_user.id).first()

    user.rendered_profile_picture = new_rendered_profile_picture
    user.profile_picture = new_profile_picture

    db.session.commit()
    return redirect(url_for('profile_bp.profile'))

def add_friend(form):

    id_for_friendship = form.id_for_friendship.data

    friend = db.session.query(User).filter_by(id_for_friendship=id_for_friendship).first()

    myself = db.session.query(User).filter_by(id=current_user.id).first()
    
    if friend in myself.friends:
        flash(friend.name + " " + friend.surname + " is already your friend", "warning")
        return redirect(url_for('profile_bp.profile'))

    myself.friends.append(friend)
    friend.friends.append(myself)

    db.session.commit()
    
    
    flash(friend.name + " " + friend.surname + " has been added to your friends", "message")
    return redirect(url_for('profile_bp.profile'))