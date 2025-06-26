from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials, initialize_app

if not firebase_admin._apps:
    cred = credentials.Certificate('/home/ubuntu/djangobackend/firstapp2/sportsforchangeproject-firebase-adminsdk-8u6av-886cee7b42.json')
    initialize_app(cred)



class Firstdemoapp2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firstdemoapp2'
