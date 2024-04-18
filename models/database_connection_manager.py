# models/database_connection_manager.py

import pymysql
import os

class DatabaseConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.getenv('DB_NAME')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = self._create_connection()

    def _create_connection(self):
        return pymysql.connect(
            host=self.host, 
            user=self.user, 
            password=self.password, 
            db=self.db,
            port=self.port,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def execute_query(self, query, args=None):
        query = query.lstrip()
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            if query.lower().startswith("select"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return True

    def get_connection(self):
        return self.connection