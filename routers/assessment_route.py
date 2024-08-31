# routers/assessment_route.py

from flask import Blueprint
from controllers.assessment_controller import AssessmentController

assessment_controller = AssessmentController()

assessment_blueprint = Blueprint('assessment_blueprint', __name__)

@assessment_blueprint.route('', methods=['POST'])
def assess_risk():
    return assessment_controller.assess_risk()