from firebase_admin import initialize_app, credentials, storage
import os

cred = credentials.Certificate('firebase-config.json')
initialize_app(cred)

firebaseBucket = os.getenv('FIREBASE_BUCKET')
bucket = storage.bucket(firebaseBucket)