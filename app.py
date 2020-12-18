from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin
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
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)
CORS(app)

app.secret_key = "asdfasdfasdfasdfasdfasdf"
login_manager.init_app(app)



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

CORS(meal, origins=['*'], supports_credentials=True)
CORS(user, origins=['*'], supports_credentials=True)
CORS(app, origins=['http://localhost:3000', 'https://dinnder-api.herokuapp.com/api/v1/meals' 'https://dinnder-react.herokuapp.com'], supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={
    r'/*': {
        'origins': '*'
    }
})
# Access-Control-Allow-Origin: 'https://dinnder-react.herokuapp.com'
# Access-Control-Allow-Origin: 'https://dinnder-api.herokuapp.com/api/v1/meals/'
# Vary: Origin

app.register_blueprint(meal, url_prefix='/api/v1/meals')
app.register_blueprint(user, url_prefix='/user')

# The default URL ends in / ("website-url/").
@app.route('/')
@cross_origin()
def index():
  my_list = ["Hey", "check", "this", "out"]
  return my_list[0]

@app.route('/sayhi/<username>')
def hello(username):
  return "Hello {}".format(username)

# @app.route('/post/<int:post_id>')
# def show_post(post_id);
# show post with given id, return post %d


if 'ON_HEROKU' in os.environ: 
  print('on heroku!')
  models.initialize()
# Run the app when the program starts!
if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)



