# yourapp/firebase_config.py
import firebase_admin
from firebase_admin import credentials

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


firebase_admin.initialize_app(credentials.ApplicationDefault())



