# routers/medical_data_route.py

from flask import Blueprint
from controllers.medical_data_controller import MedicalDataController

medical_data_controller = MedicalDataController()

medical_data_blueprint = Blueprint('medical_data_blueprint', __name__)

@medical_data_blueprint.route('/<int:med_data_id>', methods=['GET'])
def get_medical_data(med_data_id):
    return medical_data_controller.get_medical_data(med_data_id)

@medical_data_blueprint.route('/<int:med_data_id>', methods=['PUT'])
def update_medical_data(med_data_id):
    return medical_data_controller.update_medical_data(med_data_id)

@medical_data_blueprint.route('/<int:med_data_id>', methods=['DELETE'])
def delete_medical_data(med_data_id):
    return medical_data_controller.delete_medical_data(med_data_id)

@medical_data_blueprint.route('/features/<int:medical_data_id>', methods=['POST'])
def add_medical_data_features(medical_data_id):
    return medical_data_controller.add_medical_data_features(medical_data_id)

@medical_data_blueprint.route('/features/<int:medical_data_feature_id>', methods=['DELETE'])
def delete_medical_data_feature(medical_data_feature_id):
    return medical_data_controller.delete_medical_data_feature(medical_data_feature_id)

@medical_data_blueprint.route('', methods=['POST'])
def add_medical_data():
    return medical_data_controller.add_medical_data()
