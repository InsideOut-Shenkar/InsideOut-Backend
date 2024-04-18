# controllers/user_controller.py

class UserController:
    @staticmethod
    def get_user_by_id(user_id):
        return {
            "userID": user_id
        }

