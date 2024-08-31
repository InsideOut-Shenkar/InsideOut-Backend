# routers/report_route.py

from flask import Blueprint 
from controllers.report_controller import ReportController

report_controller = ReportController()

report_blueprint = Blueprint('report_blueprint', __name__)

@report_blueprint.route('/<int:report_id>', methods=['GET'])
def get_report_by_id(report_id):
    return report_controller.get_report(report_id)

@report_blueprint.route('', methods=['GET'])
def get_reports():
    return report_controller.get_reports()

@report_blueprint.route('', methods=['DELETE'])
def delete_reports():
    return report_controller.delete_reports()