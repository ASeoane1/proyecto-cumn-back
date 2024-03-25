from flask import Flask, request, jsonify
from api_logic import ApiLogic
from firebase_auth import FirebaseAuth

class ApiController:
    def __init__(self, cred_path, pyrebase_config_path):
        self.app = Flask(__name__)
        self.api_logic = ApiLogic()
        self.firebase_auth = FirebaseAuth(cred_path, pyrebase_config_path)

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/alive', 'alive', self.alive, methods=['GET'])
        self.app.add_url_rule('/auth/register', 'register', self.register_user, methods=['POST'])
        self.app.add_url_rule('/auth/authenticate', 'authenticate', self.authenticate_user, methods=['POST'])

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

    def start_server(self, port=5000):
        self.app.run(debug=True, port=port)

