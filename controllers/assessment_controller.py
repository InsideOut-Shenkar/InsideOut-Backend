# controllers/assessment_controller.py

from datetime import datetime
from flask import jsonify, request
from repositories.user_repository import UserRepository
from repositories.patient_repository import PatientRepository
from repositories.medical_data_repository import MedicalDataRepository
from repositories.report_repository import ReportRepository

from ml.risk_assessor import RiskAssessor
from ml.data_inputer import DataInputer
from ml.s3_file_manager import file_manager

columns = file_manager.fetch_json('common_columns.json')
data_inputer = DataInputer(common_columns=columns)
risk_assessor = RiskAssessor(data_inputer=data_inputer, common_columns=columns)

class AssessmentController:
    def __init__(self):
        self.user_repository = UserRepository()
        self.report_repository = ReportRepository()
        self.patient_repository = PatientRepository()
        self.medical_data_repository = MedicalDataRepository()

    def assess_risk(self):
        try:
            patient_id, user_id, medical_data_id, weights = self._validate_input()
            medical_data = self.medical_data_repository.get(medical_data_id)
            # Construct the new object
            medical_data = { item['name']: item['value'] for item in medical_data }
            risk_level, assessment_score, model_predictions = risk_assessor.calculate_risk(
                query=medical_data,
                ds2_doctor_vote=int(weights['weight_1']),
                ds4_doctor_vote=int(weights['weight_2'])
            )
            report_data = {
                'patient_id': patient_id, 'created_by': user_id,
                'medical_data_id': medical_data_id, 'risk_level': risk_level,
                'assessment_score': assessment_score, 'ds2_vote': weights['weight_1'], 'ds4_vote': weights['weight_2']
            }

            report_id = self.report_repository.add(report_data)

            for model_prediction in model_predictions:
                model_prediction_data = {
                    'model_name': model_prediction['name'], 'prediction': model_prediction['prediction'], 'model_accuracy': model_prediction['accuracy']
                }
                model_prediction_id = self.report_repository.add_model_prediction(model_prediction_data)
                report_model_prediction_data = {
                    'report_id': report_id, 'prediction_id': model_prediction_id
                }
                self.report_repository.add_report_model_prediction(report_model_prediction_data)

            return jsonify({'id': report_id}), 200
        except Exception as e:
            return jsonify({'error': 'An error occurred processing the request', 'details': str(e)}), 500

    def _validate_input(self):
        data = request.get_json()
        if not data:
            raise ValueError('No data provided')
        
        patient_id = data.get('patient_id')
        user_id = data.get('user_id')
        med_data_id = data.get('med_data_id')
        weights = data.get('weights')


        if not all([patient_id, user_id, med_data_id, weights]):
            raise ValueError('Missing data, please provide patient_id, user_id, medical_info and weights')

        return patient_id, user_id, med_data_id, weights

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