# server.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routers.user_route import user_blueprint
from routers.view_route import view_blueprint
from routers.report_route import report_blueprint
from routers.patient_route import patient_blueprint
from routers.assessment_route import assessment_blueprint
from routers.medical_data_route import medical_data_blueprint

app = Flask(__name__)

CORS(user_blueprint)
CORS(patient_blueprint)
CORS(view_blueprint)
CORS(assessment_blueprint)
CORS(medical_data_blueprint)
CORS(report_blueprint)

CORS(app, resources={
    r"/*": {
        "origins": ["https://shenkar-insideout.com"],
        "headers": "*",
        "methods": "*"
    }
})

app.register_blueprint(view_blueprint, url_prefix='/view')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(report_blueprint, url_prefix='/reports')
app.register_blueprint(patient_blueprint, url_prefix='/patients')
app.register_blueprint(assessment_blueprint, url_prefix='/assessment')
app.register_blueprint(medical_data_blueprint, url_prefix='/medical-data')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f'Error starting server: {e}')
