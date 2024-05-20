import os
from flask import Flask, request, jsonify
from api_logic import ApiLogic
from firebase_auth import FirebaseAuth
from firebase_firestore import FirebaseFirestore
from jwt_admin import JWTAdmin

class ApiController:
    def __init__(self, cred_path, pyrebase_config_path, jwt_secret_key):
        self.app = Flask(__name__)
        self.api_logic = ApiLogic()
        self.firebase_auth = FirebaseAuth(cred_path, pyrebase_config_path, jwt_secret_key)
        self.firestore_db = FirebaseFirestore(cred_path)
        self.jwt_admin = JWTAdmin(jwt_secret_key)

        self.setup_routes()
        
    def setup_routes(self):
        self.app.add_url_rule('/alive', 'alive', self.alive, methods=['GET'])
        self.app.add_url_rule('/auth/register', 'register', self.register_user, methods=['POST'])
        self.app.add_url_rule('/auth/authenticate', 'authenticate', self.authenticate_user, methods=['POST'])
        self.app.add_url_rule('/documents/get_user_documents', 'get_user_documents', self.get_user_documents, methods=['POST'])
        self.app.add_url_rule('/documents/add_user_document', 'add_user_document', self.add_user_document, methods=['POST'])
        self.app.add_url_rule('/documents/get_document', 'get_document', self.get_document, methods=['POST'])
        self.app.add_url_rule('/documents/create_update_document', 'create_update_document', self.create_update_document, methods=['POST'])
        self.app.add_url_rule('/documents/delete_user_document', 'delete_user_document', self.delete_user_document, methods=['POST'])


    def register_user(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email or password missing'}), 400
        
        response, status_code = self.firebase_auth.register_user(email, password)
        return jsonify(response), status_code

    def authenticate_user(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email or password missing'}), 400
        
        response, status_code = self.firebase_auth.authenticate_user(email, password)
        return jsonify(response), status_code

    def alive(self):
        data = self.api_logic.alive()
        return jsonify(data)

    def get_user_documents(self):
        #Validate token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        decoded_username, valid = self.jwt_admin.decode_token(token)
        if not decoded_username:
            return jsonify({'error': 'Invalid token'}), 401
        if not valid:
            if decoded_username == 'expired':
                return jsonify({'error': 'Token expired'}), 403
            elif decoded_username == 'invalid':
                return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        user = data.get('user')
        if user != decoded_username:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        #Get document names
        documents, status_code = self.firestore_db.get_documents_by_user(user)
        return jsonify(documents), status_code

    def get_document(self):
        #Validate token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        decoded_username, valid = self.jwt_admin.decode_token(token)
        if not decoded_username:
            return jsonify({'error': 'Invalid token'}), 401
        if not valid:
            if decoded_username == 'expired':
                return jsonify({'error': 'Token expired'}), 403
            elif decoded_username == 'invalid':
                return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        user = data.get('user')
        if user != decoded_username:
            return jsonify({'error': 'Unauthorized access'}), 403

        #Get document
        document_name = data.get('document_name')
        if not user or not document_name:
            return jsonify({'error': 'User or document_name missing'}), 400
        
        document, status_code = self.firestore_db.get_document(user, document_name)
        return jsonify(document), status_code

    def create_update_document(self):
        #Validate token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        decoded_username, valid = self.jwt_admin.decode_token(token)
        if not decoded_username:
            return jsonify({'error': 'Invalid token'}), 401
        if not valid:
            if decoded_username == 'expired':
                return jsonify({'error': 'Token expired'}), 403
            elif decoded_username == 'invalid':
                return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        user = data.get('user')
        if user != decoded_username:
            return jsonify({'error': 'Unauthorized access'}), 403

        #Create or update document
        document_name = data.get('document_name')
        document_data = data.get('data')
        if not user or not document_name or not document_data:
            return jsonify({'error': 'User, document_name or document_data missing'}), 400
        
        response, status_code = self.firestore_db.create_update_document(user, document_name, document_data)
        return jsonify(response), status_code
    
    def add_user_document(self):
        #Validate token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        decoded_username, valid = self.jwt_admin.decode_token(token)
        if not decoded_username:
            return jsonify({'error': 'Invalid token'}), 401
        if not valid:
            if decoded_username == 'expired':
                return jsonify({'error': 'Token expired'}), 403
            elif decoded_username == 'invalid':
                return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        user = data.get('user')
        if user != decoded_username:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        #Add user document
        document_name = data.get('document_name')
        if not user or not document_name:
            return jsonify({'error': 'User or document_name missing'}), 400
        
        response, status_code = self.firestore_db.add_user_document(user, document_name)
        return jsonify(response), status_code
    
    def delete_user_document(self):
        #Validate token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        decoded_username, valid = self.jwt_admin.decode_token(token)
        if not decoded_username:
            return jsonify({'error': 'Invalid token'}), 401
        if not valid:
            if decoded_username == 'expired':
                return jsonify({'error': 'Token expired'}), 403
            elif decoded_username == 'invalid':
                return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        user = data.get('user')
        if user != decoded_username:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        #Add user document
        document_name = data.get('document_name')
        if not user or not document_name:
            return jsonify({'error': 'User or document_name missing'}), 400
        
        response, status_code = self.firestore_db.delete_user_document(user, document_name)
        return jsonify(response), status_code

    def start_server(self, port=5000):
        if port is 0:
            #Run on cloud
            port = int(os.environ.get("PORT", 8080))
            self.app.run(debug=True, port=port, host="0.0.0.0")
        else:
            #Run locally
            self.app.run(debug=True, port=port)

