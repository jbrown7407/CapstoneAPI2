from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
import os

import models
from resources.meals import meal
from resources.users import user

login_manager = LoginManager()

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website! Restored
app = Flask(__name__)
CORS(app)
Access-Control-Allow-Origin: 'https://dinnder-api.herokuapp.com/api/v1/meals'
app.secret_key = "asdfasdfasdfasdfasdfasdf"
login_manager.init_app(app)


if 'ON_HEROKU' in os.environ:
          print('\non heroku!')
          models.initialize()                     
          # DATABASE = connect(os.environ.get('DATABASE_URL')) 
                                                  
# else:
#   DATABASE = PostgresqlDatabase('meals.sqlite')

@login_manager.user_loader
def load_user(userid):
  try:
    return models.Users.get(models.Users.id == userid)
  except models.DoesNotExist:
    return None

# Logic for our database connection
@app.before_request
def before_request():
  """Connect to the database before each request."""
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  """Close the db connection after each request."""
  g.db.close()
  return response

CORS(meal, origins='*', supports_credentials=True)
CORS(user, origins='*', supports_credentials=True)

app.register_blueprint(meal, url_prefix='/api/v1/meals')
app.register_blueprint(user, url_prefix='/user')

# The default URL ends in / ("website-url/").
@app.route('/')
def index():
  my_list = ["Hey", "check", "this", "out"]
  return my_list[0]

@app.route('/sayhi/<username>')
def hello(username):
  return "Hello {}".format(username)

# @app.route('/post/<int:post_id>')
# def show_post(post_id);
# show post with given id, return post %d

# Run the app when the program starts!
if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)