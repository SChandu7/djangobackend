import firebase_admin
from firebase_admin import credentials, messaging

# Initialize only once
if not firebase_admin._apps:
    cred = credentials.Certificate('/home/ubuntu/djangobackend/firstapp2/sportsforchangeproject-firebase-adminsdk-8u6av-886cee7b42.json')
    firebase_admin.initialize_app(cred)

# Replace this with your actual device token
device_token = 'eG1U1UTtTFGudB3xMs1c8_:APA91bFe8RA5M4jsAlcT8qDyG-DBjkvptG9wRB865n22oUib7faIpDSorNtx9N_soY-tB43X0hMCcgE7yOzR1oJlJkaU8hIaUSw-E5v7cUtp9oMPt3bgWZ8'

message = messaging.Message(
    notification=messaging.Notification(
        title='Test Message',
        body='Hello from Firebase via Python backend!',
    ),
    token=device_token,
)

try:
    response = messaging.send(message)
    print('✅ Successfully sent message:', response)
except Exception as e:
    print('❌ Error sending message:', e)
