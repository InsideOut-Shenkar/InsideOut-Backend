# controllers/user_controller.py

from flask import jsonify, request, json
from repositories.user_repository import UserRepository

class UserController:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_id(self, user_id):
        try:
            user = self.user_repository.get(user_id)
            if user:
                return jsonify(user[0]), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve user', 'details': str(e)}), 500
    
    def add_user(self):
        user_data = json.loads(request.data)
        if not user_data:
            return jsonify({'error': 'No user data provided'}), 400
        try:
            user_id = self.user_repository.add(user_data)
            return jsonify({'message': 'Patient added successfully', 'id': user_id}), 201
        except Exception as e:
            return jsonify({'error': 'Failed to add patient', 'details': str(e)}), 500

