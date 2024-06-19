# repositories/user_repository.py

from repositories.repository import Repository

class UserRepository(Repository):
    def get(self, user_id):
        query = """
            SELECT
                u.id, r.name AS role, u.full_name, u.username
            FROM
                Users u
            JOIN
                Roles r
            ON
                u.role_id = r.id
            WHERE u.id = %s
        """
        return self.db_manager.execute_query(query, (user_id,))
    
    def add(self, user_data):
        query = """
            INSERT INTO Users (role_id, full_name, username)
            VALUES (
                (SELECT id FROM Roles WHERE name = %s),
                %s, %s
            )
            RETURNING id
        """
        result = self.db_manager.execute_query(query, (
            user_data['role'],
            user_data['full_name'],
            user_data['username']
        ))
        return result[0]['id'] if result else None

    
    def update(self, user_id, update_data):
        query = """
            UPDATE Users
            SET role_id = %s, full_name = %s, username = %s
            WHERE id = %s
        """
        return self.db_manager.execute_query(query, (
            update_data['role_id'],
            update_data['full_name'],
            update_data['username'],
            user_id
        ))
    
    def delete(self, user_id):
        query = "DELETE FROM Users WHERE id = %s"
        return self.db_manager.execute_query(query, (user_id,))