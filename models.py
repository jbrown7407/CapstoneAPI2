import datetime
from peewee import *
from flask_login import UserMixin
import os

from playhouse.db_url import connect

DATABASE = PostgresqlDatabase('meals')
if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('meals.sqlite')
#acccessingg correct DB?

class User(UserMixin, Model):
    id = CharField(unique=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    favorites = CharField()
    #favorites needs to be an array
    class Meta:
        database = DATABASE
#issue here with number field??
class Meal(Model):
    id= CharField()
    meal = CharField()
    restlink = CharField()
    pic = CharField()
    
    # created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Meal], safe=True)
    print("TABLES Created")
    DATABASE.close()

    