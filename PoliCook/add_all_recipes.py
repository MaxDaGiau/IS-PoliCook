from models import Ingredient, Recipe
import base64

def add_all_recipes(app, db):
    with app.app_context():
        ingredients = [
            "Pasta",
            "Olive Oil",
            "Tomato Sauce",
            "Garlic",
            "Salt",
            "Pasta",
            "Olive Oil",
            "Tomato Sauce",
            "Pecorino cheese",
            "Salt",
            "Guanciale",
            "Egg",
            "Onions",
            "Salt",
            "Black Pepper",
            "Octopus",
            "Celery",
            "Carrot",
            "Black Pepper",
            "Salt",
            "Lemon",
            "Parsley",
            "Ingredients:",
            "Potato",
            "Garlic",
            "Rosemary",
            "Black Pepper",
            "Salt",
            "Ingredients:",
            "Flour",
            "Sugar",
            "Chocolate chips",
            "Butter",
            "Egg",
            "Salt",
            "Pasta",
            "Olive Oil",
            "Ricotta Cheese",
            "Parmigiano Cheese",
            "Cream",
            "Salt",
            "Black Pepper",
            "Rice",
            "Tomato",
            "Ham",
            "Pepper",
            "Olive",
            "Caciocavallo Cheese",
            "Peas",
            "Pickles",
            "Avocado",
            "Lime",
            "Tomato",
            "Onion",
            "Salt"
        ]


        ingredients_set = set(ingredients)

        recipes = [
            {
                "name":"Pasta with Tomato Sauce",
                "dish_type": "First Course",
                "ingredients": ["Pasta","Olive Oil","Tomato Sauce", "Garlic", "Salt"],
                "instructions": """For 4 people:<br>
                    Heat the olive oil in a pan<br><br>
                    Put the garlic and for 1 minute to aromatise<br><br>
                    Add 400 grams of tomato sauce and some salt. Cook for 30 minutes, stirring often<br><br>
                    While the tomato sauce cooks, boil some water with salt<br><br>
                    Once the water is boiling, cook 320 grams of pasta in it<br><br>
                    Once the pasta is ready put the pasta in the pan and mix it with the sauce
                """,
                "picture_path": "static/images/pasta_tomato.jpeg"
            },
            {
                "name":"Pasta Amatriciana",
                "dish_type": "First Course",
                "ingredients": ["Pasta", "Olive Oil", "Tomato Sauce", "Pecorino cheese", "Salt", "Guanciale"],
                "instructions": """For 4 people:<br>
                    Heat the olive oil in a pan<br>
                    Put the guanciale in the pan until it becomes golden<br><br>
                    Add 400 grams tomato sauce and some salt. Cook for 30 minutes, stirring often<br><br>
                    While the amatriciana cooks, boil some water with salt<br>
                    Once the water is boiling, cook 320 grams of pasta in it<br>
                    Once the pasta is ready put the pasta in the pan and mix it with amatriciana<br>
                    Grate pecorino cheese over the pasta
                """,
                "picture_path": "static/images/pasta_amatriciana.jpeg"
            },
            {
                "name":"Onion Omelette",
                "dish_type": "Second Course",
                "ingredients": ["Egg", "Olive Oil", "Onions", "Salt", "Black Pepper"],
                "instructions": """For 4 people:<br>
                        Beat 6 eggs in a bowl <br>
                        Add salt and black pepper in the bowl<br>
                        Heat the olive oil in a pan<br>
                        Cut 1 medium-sized onion in slices and put them in the pan<br>
                        Leave the onions until they get gold<br>
                        Pour the beaten eggs in the pan<br>
                        Tilt the pan slightly from one side to another to allow the eggs to cover the surface<br>
                        After 4 minutes, turn the omelette on the other side with helping yourself with the lid<br>
                        Cook other 4 minutes
                """,
                "picture_path": "static/images/onion_omelette.jpeg"
            },
            {
                "name":"Octopus Salad",
                "dish_type": "Second Course",
                "ingredients": ["Octopus", "Celery", "Carrot", "Black Pepper", "Salt", "Lemon", "Parsley"],
                "instructions": """For 4 people:<br>
                    Cut 1 celery and 1 carrot in slices<br>
                    Pour some water in a pot and add the salt<br>
                    Put celery and carrot in a pot full of water and turn on the fire<br>
                    Once the water is boiling, put 1 kilogram of octopus in it<br>
                    Cook the octopus for 45 minutes<br>
                    Once the octopus is cooked, cut it in slices<br>
                    Blend the parsley<br>
                    Squeeze some lemon and add some olive oil in the parsley<br>
                    Add some black pepper in the parsley sauce<br>
                    Mix the octopus with the parsley sauce in a bowl
                """,
                "picture_path": "static/images/octopus_salad.jpeg"
            },
            {
                "name":"Baked Potatoes",
                "dish_type": "Side Dish",
                "ingredients": ["Potato", "Garlic", "Rosemary", "Black Pepper", "Salt"],
                "instructions": """For 4 people:<br>
                    Cut 1 kilogram of potatoes in small slices<br>
                    Fill a pot with water and heat it until it boils<br>
                    Put the potatoes in the water and boil them for 5 minutes<br>
                    Put the potatoes in a bowl and mix them with salt, olive oil, garlic and rosemary<br>
                    Turn on the oven until it reaches 200 degrees<br>
                    Put the potatoes in a baking tray and then in the oven<br>
                    Cook for 20 minutes, stirring the potatoes 3 times
                """,
                "picture_path": "static/images/roasted_potatoes.jpeg"
            },
            {
                "name":"Cookies with Chocolate Chips",
                "dish_type": "Dessert",
                "ingredients": ["Flour", "Sugar", "Chocolate chips", "Butter", "Egg", "Salt"],
                "instructions": """For 4 people:<br>
                    Pour 200 grams of sugar and 100 grams of butter in a bowl<br>
                    Stir them with the electric whisk until they are well mixed<br>
                    Add 1 egg and continue to stir with the electric whisk until it is well mixed<br>
                    Add 195 grams of flour and continue stirring with the electric whisk<br>
                    Add the chocolate chips and mix with a spatula<br>
                    Take portions of the dough to make the cookies of the size you prefer<br>
                    Turn on the oven until it reaches 190 degrees<br>
                    Put the cookies in the oven and cook them for 15 minutes
                """,
                "picture_path": "static/images/chocolate_cookies.jpeg"
            },
            {
                "name":"Pasta with Ricotta Cheese",
                "dish_type": "First Course",
                "ingredients": ["Pasta", "Olive Oil", "Ricotta Cheese", "Parmigiano Cheese", "Cream", "Salt", "Black Pepper"],
                "instructions": """For 4 people:<br>
                    Fill a pot with water and starts heating it<br>
                    While the water is boiling, put 350 grams of ricotta cheese and 70 grams of cream in a bowl<br>
                    Great 70 grams of parmigiano cheese in the bowl<br>
                    Mix everything in the bowl<br>
                    Add salt and black pepper in the bowl<br>
                    Once the water is boiling, cook 320 grams of pasta in it<br>
                    Once the pasta is ready put the pasta in the the bowl containing the mix of ricotta cheese
                """,
                "picture_path": "static/images/pasta_with_ricotta.jpeg"
            },
            {
                "name":"Rice Salad",
                "dish_type": "First Course",
                "ingredients": ["Rice", "Tomato", "Ham", "Pepper", "Olive", "Caciocavallo Cheese", "Peas", "Pickles"],
                "instructions": """For 4 people:<br>
                    Fill a pot with water, put the salt and starts heating it<br>
                    Once the water is boiling, put 80 grams of peas and cook them for 3 minutes<br>
                    Once the peas are cooked, remove them and cook the rice on the same water<br>
                    Cooking the rice usually take around 13 minutes.  <br>
                    While the rice cooks, start cutting the vegetables, the ham and the cheese<br>
                    Cut in cubes 150 grams of tomato, 150 grams of peppers, 100 grams of ham, 150 grams of caciocavallo cheese, 80 grams of olives and 80 grams of pickles<br>
                    Mix all the vegetables, the cheese and the ham together<br>
                    Once the rice has been cooked, take it out from water and leave it outside until it gets cold<br>
                    Mix the rice with all the vegetables, the cheese and the ham
                """,
                "picture_path": "static/images/rice_salad.jpeg"
            },
            {
                "name":"Guacamole Sauce",
                "dish_type": "Starter",
                "ingredients": ["Avocado", "Lime", "Tomato", "Onion", "Salt"],
                "instructions": """For 4 people:<br>
                    Cut half medium-sized onion in very small parts<br>
                    Cut a tomato in cubes<br>
                    Smash 2 mature avocados<br>
                    Add salt and squeeze some lime in the avocado<br>
                    Add the onion and tomato in the avocado<br>
                    Mix everything together
                """,
                "picture_path": "static/images/guacamole.jpeg"
            }

        ]

        for i in ingredients_set:
            
            ingredient = Ingredient.query.filter_by(name=i).first()
            if ingredient is None:
                print("Adding", i)
                db.session.add(Ingredient(name=i))
                db.session.commit()

        for r in recipes:
            ingredient_objects = []
            
            for i in r['ingredients']:
                try:
                    ingredient_objects.append(Ingredient.query.filter_by(name=i).first())
                except:
                    db.session.rollback()
                    print(i, "Not found")
            
            file = open(r['picture_path'], "rb")
            picture = file.read()
            
            # Check if a recipe with that name already exists
            rec = Recipe.query.filter_by(name=r['name']).first()

            if rec is None:
            
                print("Adding", r['name'])
                recipe = Recipe(
                    name=r['name'],
                    dish_type=r['dish_type'],
                    ingredients=ingredient_objects,
                    instructions=r['instructions'],
                    picture = picture,
                    rendered_picture = base64.b64encode(picture).decode('ascii')
                )
                
                db.session.add(recipe)
                db.session.commit()

            else:
                pass