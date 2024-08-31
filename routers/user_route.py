# routers/user_route.py

from flask import Blueprint
from controllers.user_controller import UserController

user_controller = UserController()

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return user_controller.get_user_by_id(user_id)

@user_blueprint.route('', methods=['POST'])
def add_user():
    return user_controller.add_user()
