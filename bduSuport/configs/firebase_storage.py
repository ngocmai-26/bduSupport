from django.conf import settings
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate(settings.FIREBASE_CERTIFICATE)
initialize_app(
    cred, 
    {
        "storageBucket": "selina-d8690.appspot.com"
    }
)