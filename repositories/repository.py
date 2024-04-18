# repositories/repository.py

from abc import ABC, abstractmethod
from models.database_connection_manager import DatabaseConnectionManager

class Repository(ABC):
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
    
    @abstractmethod
    def get(self, id):
        """Retrieve an item by its ID"""
        pass
    
    @abstractmethod
    def add(self, item_data):
        """Add a new item to the database"""
        pass
    
    @abstractmethod
    def update(self, id, update_data):
        """Update an existing item"""
        pass
    
    @abstractmethod
    def delete(self, id):
        """Delete an item by its ID"""
        pass
