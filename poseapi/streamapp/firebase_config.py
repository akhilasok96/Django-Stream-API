import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    dir_path,
    "fitsense360-70f6f-firebase-adminsdk-jt0iu-1d8589b259.json",
)
cred = credentials.Certificate(file_path)

firebase_admin.initialize_app(cred, {"storageBucket": "fitsense360-70f6f.appspot.com"})

db = firestore.client()
bucket = storage.bucket()
