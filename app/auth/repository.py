from typing import Optional
from google.cloud.firestore import Client
from datetime import datetime
from .model import AdminModel
import logging

logger = logging.getLogger(__name__)

ADMIN_COLLECTION = "admins"


class AdminRepository:
    """Admin CRUD operations - handles all database interactions"""
    
    def __init__(self, db: Client):
        """
        Initialize repository with database client
        
        Args:
            db: Firestore database client
        """
        self.db = db
        self.collection = db.collection(ADMIN_COLLECTION)
    
    async def create(self, admin: AdminModel) -> str:
        """
        Create a new admin record
        
        Args:
            admin: AdminModel instance
            
        Returns:
            str: Document ID of created admin
            
        Raises:
            Exception: If creation fails
        """
        try:
            _, doc_ref = self.collection.add(admin.to_dict())
            logger.info(f"Admin created with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating admin: {e}")
            raise
    
    async def get_by_id(self, admin_id: str) -> Optional[AdminModel]:
        """
        Retrieve admin by ID
        
        Args:
            admin_id: Admin document ID
            
        Returns:
            Optional[AdminModel]: Admin model or None if not found
        """
        try:
            doc = self.collection.document(admin_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return AdminModel.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error retrieving admin {admin_id}: {e}")
            raise
    
    async def get_by_email(self, email: str) -> Optional[AdminModel]:
        """
        Retrieve admin by email
        
        Args:
            email: Admin email address
            
        Returns:
            Optional[AdminModel]: Admin model or None if not found
        """
        try:
            query = self.collection.where("email", "==", email.lower())
            docs = list(query.stream())
            
            if docs:
                data = docs[0].to_dict()
                data['id'] = docs[0].id
                return AdminModel.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error retrieving admin by email {email}: {e}")
            raise
    
    async def update(self, admin_id: str, update_data: dict) -> bool:
        """
        Update admin record
        
        Args:
            admin_id: Admin document ID
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if successful
            
        Raises:
            Exception: If update fails
        """
        try:
            update_data['updated_at'] = datetime.utcnow()
            self.collection.document(admin_id).update(update_data)
            logger.info(f"Admin {admin_id} updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating admin {admin_id}: {e}")
            raise
    
    async def delete(self, admin_id: str) -> bool:
        """
        Delete admin record
        
        Args:
            admin_id: Admin document ID
            
        Returns:
            bool: True if successful
        """
        try:
            self.collection.document(admin_id).delete()
            logger.info(f"Admin {admin_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting admin {admin_id}: {e}")
            raise
    
    async def email_exists(self, email: str) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            
        Returns:
            bool: True if email exists
        """
        try:
            query = self.collection.where("email", "==", email.lower())
            docs = list(query.stream())
            return len(docs) > 0
        except Exception as e:
            logger.error(f"Error checking email existence: {e}")
            raise
    
    async def list_all(self) -> list:
        """
        List all admins
        
        Returns:
            list: List of AdminModel instances
        """
        try:
            docs = self.collection.stream()
            admins = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                admins.append(AdminModel.from_dict(data))
            return admins
        except Exception as e:
            logger.error(f"Error listing admins: {e}")
            raise
