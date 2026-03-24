import firebase_admin
from firebase_admin import credentials, firestore as fb
from google.cloud.firestore import Client
from ..config.settings import settings
import logging
from typing import Optional, List, Dict, Any
import json

logger = logging.getLogger(__name__)

# Firebase Admin SDK Initialization
_db: Optional[Client] = None

def _get_firebase_credentials():
    """Create Firebase credentials from environment variables"""
    try:
        creds_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": settings.FIREBASE_CLIENT_ID,
            "auth_uri": settings.FIREBASE_AUTH_URI,
            "token_uri": settings.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL,
        }
        return credentials.Certificate(creds_dict)
    except Exception as e:
        logger.error(f"Failed to create Firebase credentials: {e}")
        raise

def init_db() -> Client:
    """Initialize Firebase connection"""
    global _db
    try:
        if not firebase_admin._apps:
            creds = _get_firebase_credentials()
            firebase_admin.initialize_app(creds)
        
        _db = fb.client()
        logger.info("Firebase Firestore connected successfully")
        return _db
    except Exception as e:
        logger.error(f"Firebase connection failed: {e}")
        raise

def get_db() -> Client:
    """Get Firestore client instance"""
    global _db
    if _db is None:
        init_db()
    return _db

class FirestoreDB:
    """Firestore Database helper class"""
    
    def __init__(self):
        self.db = get_db()
    
    async def create(self, collection: str, data: Dict[str, Any]) -> str:
        """Create a new document"""
        try:
            _, doc_ref = self.db.collection(collection).add(data)
            logger.info(f"Document created in {collection} with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating document in {collection}: {e}")
            raise
    
    async def get(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a single document"""
        try:
            doc = self.db.collection(collection).document(doc_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"Error getting document {doc_id} from {collection}: {e}")
            raise
    
    async def update(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update a document"""
        try:
            self.db.collection(collection).document(doc_id).update(data)
            logger.info(f"Document {doc_id} updated in {collection}")
            return True
        except Exception as e:
            logger.error(f"Error updating document {doc_id} in {collection}: {e}")
            raise
    
    async def delete(self, collection: str, doc_id: str) -> bool:
        """Delete a document"""
        try:
            self.db.collection(collection).document(doc_id).delete()
            logger.info(f"Document {doc_id} deleted from {collection}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id} from {collection}: {e}")
            raise
    
    async def query(self, collection: str, filter_field: str = None, filter_value: Any = None, 
                   limit: int = None) -> List[Dict[str, Any]]:
        """Query documents with optional filter"""
        try:
            query_ref = self.db.collection(collection)
            
            if filter_field and filter_value is not None:
                query_ref = query_ref.where(filter_field, "==", filter_value)
            
            if limit:
                query_ref = query_ref.limit(limit)
            
            docs = query_ref.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            return results
        except Exception as e:
            logger.error(f"Error querying {collection}: {e}")
            raise
    
    async def query_multiple(self, collection: str, filters: List[tuple] = None, 
                            limit: int = None, order_by: str = None) -> List[Dict[str, Any]]:
        """Query documents with multiple conditions"""
        try:
            query_ref = self.db.collection(collection)
            
            if filters:
                for field, operator, value in filters:
                    query_ref = query_ref.where(field, operator, value)
            
            if order_by:
                query_ref = query_ref.order_by(order_by)
            
            if limit:
                query_ref = query_ref.limit(limit)
            
            docs = query_ref.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            return results
        except Exception as e:
            logger.error(f"Error querying {collection} with multiple filters: {e}")
            raise
    
    async def set_document(self, collection: str, doc_id: str, data: Dict[str, Any], merge: bool = True) -> bool:
        """Set/replace a document"""
        try:
            self.db.collection(collection).document(doc_id).set(data, merge=merge)
            logger.info(f"Document {doc_id} set in {collection}")
            return True
        except Exception as e:
            logger.error(f"Error setting document {doc_id} in {collection}: {e}")
            raise
    
    async def batch_write(self, operations: List[tuple]) -> bool:
        """Batch write operations (create, update, delete)"""
        try:
            batch = self.db.batch()
            
            for operation in operations:
                if operation[0] == 'set':
                    _, collection, doc_id, data = operation
                    batch.set(self.db.collection(collection).document(doc_id), data)
                elif operation[0] == 'update':
                    _, collection, doc_id, data = operation
                    batch.update(self.db.collection(collection).document(doc_id), data)
                elif operation[0] == 'delete':
                    _, collection, doc_id = operation
                    batch.delete(self.db.collection(collection).document(doc_id))
            
            batch.commit()
            logger.info(f"Batch write completed with {len(operations)} operations")
            return True
        except Exception as e:
            logger.error(f"Error in batch write: {e}")
            raise

# Global instance
fs_db = FirestoreDB()

async def get_firebase_db() -> FirestoreDB:
    """Dependency injection for Firestore DB"""
    return fs_db
