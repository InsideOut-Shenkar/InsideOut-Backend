# controllers/medical_data_controller.py

from flask import jsonify, request
from repositories.medical_data_repository import MedicalDataRepository

class MedicalDataController:
    def __init__(self):
        self.medical_data_repository = MedicalDataRepository()
    
    def add_medical_data(self):
        data = request.get_json()
        if not data or not all(key in data for key in ['medical_info', 'patient_id']):
            return jsonify({'error': 'Missing data, please provide medical_info and patient_id'}), 400

        try:
            med_data_id = self.medical_data_repository.add(data['patient_id'])
            if med_data_id is None:
                raise ValueError('Failed to create medical data record.')

            failed_features = []
            for feature in data['medical_info']:
                feature_id = self.medical_data_repository.add_feature(feature, data['medical_info'][feature])
                if not feature_id:
                    failed_features.append(feature)

                if not self.medical_data_repository.add_meds_feature(med_data_id, feature_id):
                    failed_features.append(feature)
            
            if failed_features:
                return jsonify({'error': 'Failed to add some features', 'details': failed_features}), 400

            return jsonify({'message': 'Medical data added successfully', 'id': med_data_id}), 201
        except Exception as e:
            return jsonify({'error': 'Failed to add medical data', 'details': str(e)}), 500

    def add_medical_data_features(self, medical_data_id):
        data = request.get_json()
        if not data or not all(key in data for key in ['medical_info']):
            return jsonify({'error': 'Missing data, please provide both medical_info and med_data_id'}), 400

        features = data['medical_info']

        try:
            failed_features = []
            for feature in features:
                feature_id = self.medical_data_repository.add_feature(feature)
                if not feature_id:
                    failed_features.append(feature)
                    continue 

                if not self.medical_data_repository.add_meds_feature(medical_data_id, feature_id):
                    failed_features.append(feature)

            if failed_features:
                return jsonify({'error': 'Failed to add some features', 'details': failed_features}), 400

            return jsonify({'message': 'Medical data features added successfully'}), 201

        except Exception as e:
            return jsonify({'error': 'An internal error occurred while adding medical data features', 'details': str(e)}), 500

    def get_medical_data(self, med_data_id):
        try:
            data = self.medical_data_repository.get(med_data_id)
            if data is None:
                return jsonify({'error': 'Medical data not found'}), 404
            return jsonify(data), 200
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve medical data', 'details': str(e)}), 500

    def update_medical_data(self, med_data_id):
        update_data = request.get_json()
        if not update_data:
            return jsonify({'error': 'No update data provided'}), 400

        try:
            updated_data = self.medical_data_repository.update(med_data_id, update_data)
            if updated_data is None:
                return jsonify({'error': 'Medical data not found'}), 404
            return jsonify(updated_data), 200
        except Exception as e:
            return jsonify({'error': 'Failed to update medical data', 'details': str(e)}), 500

    def delete_medical_data(self, med_data_id):
        try:
            result = self.medical_data_repository.delete(med_data_id)
            if not result:
                return jsonify({'error': 'Medical data not found'}), 404
            return jsonify({'message': 'Medical data deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to delete medical data', 'details': str(e)}), 500

    def delete_medical_data_feature(self, medical_data_feature_id):
        try:
            result = self.medical_data_repository.delete_feature(medical_data_feature_id)
            if not result:
                return jsonify({'error': 'Medical data feature not found'}), 404
            return jsonify({'message': 'Medical data feature deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to delete medical data feature', 'details': str(e)}), 500
