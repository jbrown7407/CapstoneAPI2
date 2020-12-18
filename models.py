import datetime
from peewee import *
from flask_login import UserMixin
import os

from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.eviron.get('HEROKU_POSTGRESQL_RED_URL'))
else:
    DATABASE = {*whatever you already had as your DATABASE*}

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

    