# yourapp/firebase_config.py
import firebase_admin
from firebase_admin import credentials

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cred = credentials.Certificate(os.path.join(BASE_DIR, 'firstapp2', 'sportsforchange-35208-firebase-adminsdk-vs78f-4ba6d80413.json'))


