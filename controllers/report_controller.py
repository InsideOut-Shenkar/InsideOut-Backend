# controllers/report_controller.py

from flask import jsonify, request, json
from repositories.report_repository import ReportRepository

class ReportController:
    def __init__(self):
        self.report_repository = ReportRepository()

    def get_report(self, report_id):
        try:
            report = self.report_repository.get(report_id)
            if report:
                return jsonify(report[0]), 200
            else:
                return jsonify({'error': 'Report not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve report', 'details': str(e)}), 500
        
    def get_reports(self):
        try:
            reports = self.report_repository.get_reports()
            if reports:
                return jsonify(reports), 200
            else:
                return jsonify({'error': 'No reports found'}), 404
        except Exception as e:
            return jsonify({'error': 'An error occurred while fetching reports', 'details': str(e)}), 500
