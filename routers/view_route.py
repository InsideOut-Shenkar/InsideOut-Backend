# routers/view_route.py

from flask import Blueprint
from controllers.patient_controller import PatientController

patient_controller = PatientController()

view_blueprint = Blueprint('view_blueprint', __name__)

@view_blueprint.route('/patients/<int:user_id>', methods=['GET'])
def get_patients_list_by_user_id(user_id):
    return patient_controller.get_patients_list_by_user_id(user_id)

@view_blueprint.route('/patients', methods=['GET'])
def get_patients_list():
    return patient_controller.get_patients_list()
