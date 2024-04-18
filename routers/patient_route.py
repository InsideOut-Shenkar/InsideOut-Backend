# routers/patient_route.py

from flask import Blueprint, request, jsonify, json
from controllers.patient_controller import PatientController

patient_controller = PatientController()

patient_blueprint = Blueprint('patient_blueprint', __name__)

@patient_blueprint.route('/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    return patient_controller.get_patient(patient_id)

@patient_blueprint.route('', methods=['GET'])
def get_patients():
    return patient_controller.get_patients()

@patient_blueprint.route('', methods=['POST'])
def add_patient():
    return patient_controller.add_patient()

@patient_blueprint.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    return patient_controller.update_patient(patient_id)

@patient_blueprint.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    return patient_controller.delete_patient(patient_id)

@patient_blueprint.route('', methods=['DELETE'])
def delete_patients():
    return patient_controller.delete_patients()