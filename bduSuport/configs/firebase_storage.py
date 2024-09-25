from django.conf import settings
from firebase_admin import credentials, initialize_app

import os
print("Current working directory:", os.getcwd())
cred = credentials.Certificate(settings.FIREBASE_CERTIFICATE)
initialize_app(
    cred, 
    {
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET_URL
    }
)