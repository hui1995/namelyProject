from django.db import models
import mongoengine

# Create your models here.
class UserModel(mongoengine.Document):
    email = mongoengine.StringField(primary_key=True,max_length=30)
    username = mongoengine.StringField(max_length=30)
    password = mongoengine.StringField(max_length=30)
    meta = {'collection':'zc_items', 'strict': False}

