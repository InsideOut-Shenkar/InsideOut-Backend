# repositories/medical_data_repository.py

from repositories.repository import Repository

class MedicalDataRepository(Repository):
    def get(self, med_data_id):
        query = """
            SELECT 
                md.*,
                mdf.name,
                mdf.value
            FROM 
                Medical_Data md
            JOIN 
                Medical_Data_Features mdfs 
            ON
                md.id = mdfs.medical_data_id
            JOIN
                Medical_Data_Feature mdf
            ON
                mdf.id = mdfs.medical_data_feature_id
            WHERE md.id = %s
        """
        return self.db_manager.execute_query(query, (med_data_id))

    def add(self, patient_id):
        insert_query = """
            INSERT INTO Medical_Data (patient_id) 
            VALUES (%s)
        """
        self.db_manager.execute_query(insert_query, (patient_id))

        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None

    def add_feature(self, item_data_key, item_data_value):
        insert_query = """
            INSERT INTO Medical_Data_Feature (name, value) 
            VALUES (%s, %s)
        """
        self.db_manager.execute_query(insert_query, (item_data_key, item_data_value))
        
        id_query  = "SELECT LAST_INSERT_ID()"
        result = self.db_manager.execute_query(id_query)
        return result[0]['LAST_INSERT_ID()'] if result else None

    def add_meds_feature(self, med_data_id, med_data_feature_id):
        query = """
            INSERT INTO Medical_Data_Features (medical_data_id, medical_data_feature_id)
            VALUES (%s, %s)
        """
        return self.db_manager.execute_query(query, (med_data_id, med_data_feature_id))

    def update(self, id, update_data):
        """No need for updating an existing item"""
        pass
    
    def delete(self, med_data_id):
        query = "DELETE FROM Medical_Data WHERE id = %s"
        return self.db_manager.execute_query(query, (med_data_id))

    def delete_feature(self, medical_data_feature_id):
        query = "DELETE FROM Medical_Data_Feature WHERE id = %s"
        return self.db_manager.execute_query(query, (medical_data_feature_id))
             