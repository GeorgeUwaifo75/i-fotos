import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "your-bucket-name.appspot.com",
    'databaseURL': "https://your-project.firebaseio.com"
})
db = firestore.client()
bucket = storage.bucket()
