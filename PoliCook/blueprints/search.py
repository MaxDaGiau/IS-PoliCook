from flask import request, Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField, SubmitField
from models import Ingredient, Recipe, RecipeVariation, User
from flask_login import current_user
import json

search_blueprint = Blueprint("search_bp", __name__)

class SearchForm(FlaskForm):
    ingredients_list = HiddenField(id="ingredients_list")
    submit = SubmitField()
    dish_type = RadioField(default="All", choices=[
        "All",
        "Starter",
        "First Course",
        "Second Course",
        "Side Dish",
        "Dessert"])


@search_blueprint.route('/search', methods=['POST', 'GET'])
def search():
    
    ingredients = [x.name for x in Ingredient.query.all()]

    ingredients = []

    for x in Ingredient.query.all():
        ingredients.append(x.name)

    format_ingredients = [x.lower().capitalize() for x in ingredients]

    all_ingredients = sorted(format_ingredients)

    search_form = SearchForm()

    if search_form.validate_on_submit():
        selected_ingredients = search_form.ingredients_list.data
        
        if selected_ingredients.strip() == "":
            selected_ingredients = []
        else:
            selected_ingredients = selected_ingredients.split(',')

        dish_type = search_form.dish_type.data

        results = get_results(selected_ingredients, dish_type)
        search_form.ingredients_list.data = ""

        return render_template("search_page.html", all_ingredients=all_ingredients, dish_type=dish_type, results=results, user=current_user, form=search_form)
    else:
        return render_template("search_page.html", all_ingredients=all_ingredients, results=None, user=current_user, form=search_form)



def get_results(selected_ingredients, dish_type):

    results = []

    if dish_type != "All":
        recipes = Recipe.query.filter_by(dish_type=dish_type)
    else:
        recipes = Recipe.query.all()


    to_search_recipes = []
    
    for r in recipes:
        
        ingredients_in_common = 0

        user_ingredients = []
        for s in selected_ingredients:
            user_ingredients.append(s.lower())

        for ing in r.ingredients:
            if ing.name.lower() in user_ingredients:
                ingredients_in_common += 1

        if ingredients_in_common == len(selected_ingredients):
            to_search_recipes.append(r)
            
    sorted_recipes = sorted(to_search_recipes, key=lambda x: len(x.ingredients))
    
    for recipe in sorted_recipes:
        
        if current_user.is_authenticated:
            friends_who_commented = get_friends_who_commented(recipe)
            comment_message = get_friends_comment_message(friends_who_commented)
        else:
            comment_message = ""

        results.append(
            {
                "recipe": recipe,
                "comment_message": comment_message
                })

    return results

def get_friends_who_commented(recipe):

    comments = RecipeVariation.query.filter_by(recipe_id=recipe.id).all()

    friends_who_commented = []

    all_friends_ids = [friend.id for friend in current_user.friends]
    
    for c in comments:
        if c.user_id in all_friends_ids and c.user_id not in friends_who_commented:
            friends_who_commented.append(c.user_id)

    return friends_who_commented

def get_friends_comment_message(friends):
    
    suffix = " shared their variation on this recipe! Check it out"

    if len(friends) > 3:
        message = get_name_and_lastname(friends[0]) + ", " + get_name_and_lastname(friends[1]) + " and other " + len(friends) - 2 + suffix

    elif len(friends) == 3:
        message = get_name_and_lastname(friends[0]) + ", " + get_name_and_lastname(friends[1]) + " and " + get_name_and_lastname(friends[2]) + suffix
    
    elif len(friends) == 2:    
        message = get_name_and_lastname(friends[0]) + " and " + get_name_and_lastname(friends[1]) + suffix

    elif len(friends) == 1:
        message = get_name_and_lastname(friends[0]) + " shared its variation on this recipe! Check it out"

    else:
        message = "None of your friends shared their variation on this recipe yet, be the first!"

    return message

def get_name_and_lastname(user):
    return User.query.get(user).name + " " + User.query.get(user).surname