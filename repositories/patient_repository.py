# repositories/patient_repository.py
from repositories.repository import Repository

class PatientRepository(Repository):
    def get(self, patient_id):
        query = "SELECT * FROM Patients WHERE id = %s"
        return self.db_manager.execute_query(query, (patient_id))
    
    def get_by_id_number(self, id_number):
        query = "SELECT * FROM Patients WHERE id_number = %s"
        return self.db_manager.execute_query(query, (id_number,))

    def get_patients(self):
        query = "SELECT * FROM Patients"
        return self.db_manager.execute_query(query)
    
    def add(self, patient_data):
        insert_query  = """
            INSERT INTO Patients (id_number, date_of_birth, created_by)
            VALUES (%s, %s, %s)
        """
        self.db_manager.execute_query(insert_query, (patient_data['id_number'], patient_data['date_of_birth'], patient_data['created_by']))

        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None
    

    def update(self, id_number, update_data):
        query = "UPDATE Patients SET date_of_birth = %s, created_by = %s WHERE id_number = %s"
        return self.db_manager.execute_query(query, (update_data['date_of_birth'], update_data['created_by'], id_number))

    def delete(self, id_number):
        query = "DELETE FROM Patients WHERE id_number = %s"
        return self.db_manager.execute_query(query, (id_number))
    
    def delete_patients(self, id_numbers):
        id_numbers_tuple = tuple(id_numbers)
        placeholders = ', '.join(['%s'] * len(id_numbers_tuple))
        query = f"DELETE FROM Patients WHERE id_number IN ({placeholders})"
        return self.db_manager.execute_query(query, id_numbers_tuple)

    def get_patients_list_by_user_id(self, user_id):
        query = """
            SELECT 
                Patients.id
                Patients.id_number, 
                Patients.date_of_birth, 
                Users.full_name,
                COUNT(Reports.id) AS report_count
            FROM 
                Patients 
            JOIN 
                Users ON Patients.created_by = Users.id 
            LEFT JOIN 
                Reports ON Patients.id = Reports.patient_id
            WHERE 
                Users.id = %s
            GROUP BY 
                Patients.id
        """
        return self.db_manager.execute_query(query, (user_id))
    
    def get_patients_list(self):
        query = """
            SELECT 
                Patients.id,
                Patients.id_number, 
                Patients.date_of_birth, 
                Users.full_name,
                COUNT(Reports.id) AS report_count
            FROM 
                Patients 
            JOIN 
                Users ON Patients.created_by = Users.id 
            LEFT JOIN 
                Reports ON Patients.id = Reports.patient_id
            GROUP BY 
                Patients.id
        """
        return self.db_manager.execute_query(query, ())
