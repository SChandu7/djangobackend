import firebase_admin
from firebase_admin import credentials, messaging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate('/home/ubuntu/djangobackend/firstapp2/sportsforchange-35208-firebase-adminsdk-vs78f-5ee47c01ba.json')
    firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
    exit(1)

# Test sending a single notification
def send_test_notification():
    # Replace with a valid FCM device token from your /getsportsnotificationtoken/ endpoint
    device_token = "replace-with-valid-device-token"
    
    message = messaging.Message(
        notification=messaging.Notification(
            title="Test Notification",
            body="This is a test message from your EC2 instance"
        ),
        token=device_token
    )
    
    try:
        response = messaging.send(message)
        logger.info(f"Successfully sent message: {response}")
        return response
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return None

if __name__ == "__main__":
    send_test_notification()
