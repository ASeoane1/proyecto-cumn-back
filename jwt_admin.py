import jwt

class JWTAdmin:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self, username):
        payload = {'user': f'{username}'}
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def decode_token(self, token):
        try:
            if token.startswith('Bearer '):
                token = token[len('Bearer '):]
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            username = decoded_payload['user']
            return username, True
        except jwt.ExpiredSignatureError:
            return 'expired' , False
        except (jwt.InvalidTokenError, KeyError):
            return 'invalid' , False
