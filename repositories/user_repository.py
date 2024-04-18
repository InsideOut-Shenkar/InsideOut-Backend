# repositories/user_repository.py

from repositories.repository import Repository

class UserRepository(Repository):
    def get(self, user_id):
        query = """
            SELECT user_id, rule_id, full_name, username
            FROM Users
            WHERE user_id = %s
        """
        return self.db_manager.execute_query(query, (user_id,))
    
    def add(self, user_data):
        query = """
            INSERT INTO Users (rule_id, full_name, username, hashed_password, salt)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db_manager.execute_query(query, (
            user_data['rule_id'],
            user_data['full_name'],
            user_data['username'],
            user_data['hashed_password'],
            user_data['salt']
        ))
    
    def update(self, user_id, update_data):
        query = """
            UPDATE Users
            SET rule_id = %s, full_name = %s, username = %s
            WHERE user_id = %s
        """
        return self.db_manager.execute_query(query, (
            update_data['rule_id'],
            update_data['full_name'],
            update_data['username'],
            user_id
        ))
    
    def delete(self, user_id):
        query = "DELETE FROM Users WHERE user_id = %s"
        return self.db_manager.execute_query(query, (user_id,))