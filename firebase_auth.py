import pyrebase
import json
from jwt_admin import JWTAdmin

class FirebaseAuth:
    def __init__(self, cred_path, firebase_config_path, jwt_secret_key):
        self.cred_path = cred_path
        self.firebase_config_path = firebase_config_path
        self.jwt_admin = JWTAdmin(jwt_secret_key)
        self.initialize_firebase()

    def initialize_firebase(self):
        # Load config
        with open(self.firebase_config_path) as config_file:
            firebase_config = json.load(config_file)

        # Initiazize pyrebase
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.firebase_auth = self.firebase.auth()

    def register_user(self, email, password):
        try:
            user = self.firebase_auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            return {'message': 'User sign up successful', 'user_id': user_id}, 200
        except Exception as e:
            error_message = e.args[1]
            return {'error': error_message}, 400

    def authenticate_user(self, email, password):
        try:
            user = self.firebase_auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']
            # Generate token
            token = self.jwt_admin.generate_token(user_id)
            
            return {'message': 'Login successful', 'user_id': user_id, 'token': token}, 200
        except Exception as e:
            error_message = e.args[1]
            return {'error': error_message}, 400
