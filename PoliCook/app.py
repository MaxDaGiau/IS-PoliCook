from flask import Flask
from flask_login import LoginManager
from models import *
from add_all_recipes import add_all_recipes
from blueprints import *

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///policook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'the random string'


# this variable, db, will be used for all SQLAlchemy commands
with app.app_context():
    db.init_app(app)
    db.create_all()

add_all_recipes(app, db)

app.register_blueprint(search_blueprint)
app.register_blueprint(add_comment_blueprint)
app.register_blueprint(homepage_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(profile_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8888, debug=True)