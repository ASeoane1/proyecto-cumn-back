import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseFirestore:
    def __init__(self, cred_path):
        self.cred_path = cred_path
        self.initialize_firebase()
    
    def initialize_firebase(self):
        cred = credentials.Certificate(self.cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_documents_by_user(self, user):
        try:
            user_documents = self.db.collection('collection').document(user).get()
            if user_documents.exists:
                return user_documents.to_dict().values(), 200
            else:
                return [] , 201
        except Exception as e:
            return "Error getting documents by user: {}".format(e), 500

    def add_user_document(self, user, document_name):
        try:
            document = self.db.collection(user).document(user)
            if document.get().exists:
                user_documents = self.get_documents_by_user(user)
                if document_name in user_documents:
                    return "Document already exists", 401
                else:
                    document.set({document_name: document_name}, merge=True)
                    return "Document added successfully", 200
            else:
                new_document = self.db.collection('collection').document(user)
                new_document.set({document_name: document_name}, merge=True)
                return "Document added successfully", 200
        except Exception as e:
            return "Error adding user document: {}".format(e), 500

    def get_document(self, user, document_name):
        try:
            document = self.db.collection('collection').document(user + '_' + document_name).get()
            if document.exists:
                return document.to_dict(), 200
            else:
                return {} , 201
        except Exception as e:
            return "Error getting document: {}".format(e), 500

    def create_update_document(self, user, document_name, data):
        try:
            document = self.db.collection('collection').document(user + '_' + document_name)
            if document.get().exists:
                document.set(data)
                return "Document updated successfully", 200
            else:
                new_document = self.db.collection('collection').document(user + '_' + document_name)
                new_document.set(data)
                return "Document created successfully", 200
        except Exception as e:
            return "Error creating or updating document: {}".format(e), 500
