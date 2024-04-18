# controllers/patient_controller.py

from flask import jsonify, request, json
from repositories.patient_repository import PatientRepository

class PatientController:
    def __init__(self):
        self.patient_repository = PatientRepository()

    def get_patient(self, patient_id):
        try:
            patient = self.patient_repository.get(patient_id)
            if patient:
                return jsonify(patient), 200
            else:
                return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve patient', 'details': str(e)}), 500

    def get_patients(self):
        try:
            patients = self.patient_repository.get_patients()
            if patients:
                return jsonify(patients), 200
            else:
                return jsonify({'error': 'No patients found'}), 404
        except Exception as e:
            return jsonify({'error': 'An error occurred while fetching patients', 'details': str(e)}), 500

    def add_patient(self):
        patient_data = json.loads(request.data)
        if not patient_data:
            return jsonify({'error': 'No patient data provided'}), 400
        try:
            patient_id = self.patient_repository.add(patient_data)
            return jsonify({'message': 'Patient added successfully', 'id': patient_id}), 201
        except Exception as e:
            return jsonify({'error': 'Failed to add patient', 'details': str(e)}), 500

    def update_patient(self, patient_id):
        update_data = json.loads(request.data)
        if not update_data:
            return jsonify({'error': 'No update data provided'}), 400
        try:
            updated_patient = self.patient_repository.update(patient_id, update_data)
            if updated_patient:
                return jsonify(updated_patient), 200
            else:
                return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to update patient', 'details': str(e)}), 500

    def delete_patient(self, id_number):
        if not id_number:
            return jsonify({'error': 'No patient ID provided'}), 400
        try:
            result = self.patient_repository.delete(id_number)
            if result:
                return jsonify({'message': 'Patient deleted successfully'}), 200
            else:
                return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to delete patient', 'details': str(e)}), 500
        
    def delete_patients(self):
        id_numbers = json.loads(request.data)
        if not id_numbers:
            return jsonify({'error': 'No patient IDs provided'}), 400
        try:
            result = self.patient_repository.delete_patients(id_numbers)
            if result:
                return jsonify({'message': 'Patients deleted successfully'}), 200
            else:
                return jsonify({'error': 'Patients not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to delete patients', 'details': str(e)}), 500
        
    def get_patients_list(self):
        try:
            patients = self.patient_repository.get_patients_list()
            if patients:
                return jsonify(patients), 200
            else:
                return jsonify({'error': 'No patients found'}), 404
        except Exception as e:
            return jsonify({'error': 'An error occurred while fetching patients', 'details': str(e)}), 500
    
    def get_patients_list_by_user_id(self, user_id):
        try:
            patients = self.patient_repository.get_patients_list_by_user_id(user_id)
            if patients:
                return jsonify(patients), 200
            else:
                return jsonify({'error': 'No patients found for provided user ID'}), 404
        except Exception as e:
            return jsonify({'error': 'An error occurred while fetching patients', 'details': str(e)}), 500
