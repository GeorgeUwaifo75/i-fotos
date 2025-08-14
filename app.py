import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "your-bucket-name.appspot.com",
    'databaseURL': "https://your-project.firebaseio.com"
})
db = firestore.client()
bucket = storage.bucket()


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    photo = request.files['photo']
    user_id = request.form.get('user_id')
    
    # Upload to Firebase Storage
    blob = bucket.blob(f"photos/{user_id}/{photo.filename}")
    blob.upload_from_file(photo)
    blob.make_public()
    
    # Save metadata to Firestore
    db.collection('photos').add({
        'user_id': user_id,
        'url': blob.public_url,
        'upvotes': 0,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    
    return jsonify({"url": blob.public_url})
