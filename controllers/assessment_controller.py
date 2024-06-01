# controllers/assessment_controller.py

from datetime import datetime
from flask import jsonify, request
from repositories.patient_repository import PatientRepository
from repositories.user_repository import UserRepository
from ml.prediction import calculate_risk

class AssessmentController:
    def __init__(self):
        self.patient_repository = PatientRepository()
        self.user_repository = UserRepository()

    def assess_risk(self):
        try:
            patient_id, user_id, medical_info = self._validate_input()
            patient = self._get_patient(patient_id)
            user = self._get_user(user_id)[0]
            if 'age' not in medical_info:
                medical_info['age'] = self._calculate_age(patient['date_of_birth'])
            risk_assessment = calculate_risk(medical_info)
            return jsonify(risk_assessment), 200
        except Exception as e:
            return jsonify({'error': 'An error occurred processing the request', 'details': str(e)}), 500

    def _validate_input(self):
        data = request.get_json()
        if not data:
            raise ValueError('No data provided')
        
        patient_id = data.get('patient_id')
        user_id = data.get('user_id')
        medical_info = data.get('medical_info')

        if not all([patient_id, user_id, medical_info]):
            raise ValueError('Missing data, please provide patient_id, user_id, and medical_info')

        return patient_id, user_id, medical_info

    def _get_patient(self, patient_id):
        patient = self.patient_repository.get(patient_id)
        if not patient:
            raise ValueError(f"No patient found with ID {patient_id}")
        return patient

    def _get_user(self, user_id):
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError(f"No user found with ID {user_id}")
        return user
    
    def _calculate_age(self, birthdate):
        today = datetime.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))