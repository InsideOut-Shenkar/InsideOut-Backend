# repositories/report_repository.py

from repositories.repository import Repository

class ReportRepository(Repository):
    def get(self, report_id):
        query = """
            SELECT 
                re.id, actual_risk, assessment_score, ri.risk_level as risk_level_label,
                re.created_at, re.created_by, ds2_vote, ds4_vote, medical_data_id, modified_at,
                patient_id, p.id_number
            FROM 
                Reports re
            JOIN
                Risks ri
            ON
                re.risk_level = ri.id
            JOIN
                Patients p
            ON
                re.patient_id = p.id
            WHERE re.id = %s
        """
        return self.db_manager.execute_query(query, (report_id))
    
    def get_reports(self):
        query = """
            SELECT 
                re.id, actual_risk, assessment_score, ri.risk_level as risk_level_label,
                re.created_at, u.full_name, ds2_vote, ds4_vote, medical_data_id, modified_at,
                patient_id, p.id_number
            FROM 
                Reports re
            JOIN
                Risks ri
            ON
                re.risk_level = ri.id
            JOIN
                Users u
            ON
                re.created_by = u.id
            JOIN
                Patients p
            ON
                re.patient_id = p.id
        """
        return self.db_manager.execute_query(query)

    def add(self, report_data):
        query = """
            INSERT INTO Reports (patient_id, created_by, medical_data_id, risk_level, 
                                assessment_score, ds2_vote, ds4_vote) 
            VALUES (%s, %s, %s, (SELECT id FROM Risks WHERE risk_level = %s), %s, %s, %s)
        """
        self.db_manager.execute_query(query, (
            report_data['patient_id'], report_data['created_by'], report_data['medical_data_id'],
            report_data['risk_level'], report_data['assessment_score'], report_data['ds2_vote'], report_data['ds4_vote']
        ))
        
        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None
    
    def add_model_prediction(self, model_prediction_data):
        query = """
            INSERT INTO Model_Predictions (model_name, prediction, model_accuracy) 
            VALUES (%s, %s, %s)
        """
        self.db_manager.execute_query(query, (
            model_prediction_data['model_name'], model_prediction_data['prediction'], 
            model_prediction_data['model_accuracy']
        ))
        
        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None
    
    def add_report_model_prediction(self, report_model_prediction_data):
        query = """
            INSERT INTO Report_Model_Predictions (report_id, prediction_id) 
            VALUES (%s, %s)
        """
        self.db_manager.execute_query(query, (
            report_model_prediction_data['report_id'], report_model_prediction_data['prediction_id']
        ))
        
        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None
    
    def update(self, report_id, update_data):
        """ NO NEED TO UPDATE A REPORT"""
        pass
        
    def delete(self, report_id):
        query = """
            DELETE FROM Reports WHERE id = %s
        """
        return self.db_manager.execute_query(query, (report_id))
    
    def delete_reports(self, reports_ids):
        ids_tuple = tuple(reports_ids)
        placeholders = ', '.join(['%s'] * len(ids_tuple))
        query = f"DELETE FROM Reports WHERE id IN ({placeholders})"
        return self.db_manager.execute_query(query, ids_tuple)
