# models/database_connection_manager.py

import psycopg2
import psycopg2.extras
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
        self.port = int(os.getenv('DB_PORT', 5432))
        self.connection = self._create_connection()

    def _create_connection(self):
        return psycopg2.connect(
            host=self.host, 
            user=self.user, 
            password=self.password, 
            dbname=self.db,
            port=self.port,
            cursor_factory=psycopg2.extras.DictCursor
        )
    
    def execute_query(self, query, args=None):
        try:
            query = query.lstrip()
            with self.connection.cursor() as cursor:
                cursor.execute(query, args)
                if query.lower().startswith("select"):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return True
        except psycopg2.OperationalError as e:
            if e.pgcode in ('08006', '08003'):
                self.connection = self._create_connection()
                return self.execute_query(query, args)
            else:
                raise

    def get_connection(self):
        return self.connection
