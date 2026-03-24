import firebase_admin
from firebase_admin import storage
from ..config.settings import settings
import logging
from typing import Optional
import io
from datetime import datetime

logger = logging.getLogger(__name__)

class FirebaseStorage:
    """Firebase Storage helper class for handling images and files"""
    
    def __init__(self):
        try:
            if not firebase_admin._apps:
                from firebase_admin import credentials
                from ..config.settings import settings
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
                creds = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(creds, {'storageBucket': settings.FIREBASE_STORAGE_BUCKET})
            
            self.bucket = storage.bucket()
            logger.info("Firebase Storage initialized successfully")
        except Exception as e:
            logger.error(f"Firebase Storage initialization failed: {e}")
            raise
    
    async def upload_file(self, file_bytes: bytes, destination_path: str, 
                         content_type: str = "application/octet-stream") -> str:
        """
        Upload a file to Firebase Storage
        Args:
            file_bytes: File content as bytes
            destination_path: Path where file will be stored (e.g., 'shipment_labels/label_123.pdf')
            content_type: MIME type of the file
        Returns:
            Public URL of the uploaded file
        """
        try:
            blob = self.bucket.blob(destination_path)
            blob.upload_from_string(file_bytes, content_type=content_type)
            blob.make_public()
            logger.info(f"File uploaded to {destination_path}")
            return blob.public_url
        except Exception as e:
            logger.error(f"Error uploading file to {destination_path}: {e}")
            raise
    
    async def upload_image(self, file_bytes: bytes, entity_type: str, entity_id: str, 
                          filename: str) -> str:
        """
        Upload an image file
        Args:
            file_bytes: Image content as bytes
            entity_type: Type of entity (e.g., 'customer', 'shipment', 'agent')
            entity_id: ID of the entity
            filename: Original filename
        Returns:
            Public URL of the uploaded image
        """
        try:
            # Create organized path: images/{entity_type}/{entity_id}/{timestamp}_{filename}
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            destination_path = f"images/{entity_type}/{entity_id}/{timestamp}_{filename}"
            
            # Determine content type based on file extension
            extension = filename.lower().split('.')[-1] if '.' in filename else 'jpg'
            content_types = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            content_type = content_types.get(extension, 'image/jpeg')
            
            blob = self.bucket.blob(destination_path)
            blob.upload_from_string(file_bytes, content_type=content_type)
            blob.make_public()
            logger.info(f"Image uploaded to {destination_path}")
            return blob.public_url
        except Exception as e:
            logger.error(f"Error uploading image for {entity_type}/{entity_id}: {e}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from Firebase Storage"""
        try:
            blob = self.bucket.blob(file_path)
            blob.delete()
            logger.info(f"File deleted from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise
    
    async def get_file_url(self, file_path: str) -> str:
        """Get public URL for a file"""
        try:
            blob = self.bucket.blob(file_path)
            url = blob.public_url
            logger.info(f"Retrieved URL for {file_path}")
            return url
        except Exception as e:
            logger.error(f"Error getting URL for {file_path}: {e}")
            raise
    
    async def download_file(self, file_path: str) -> bytes:
        """Download a file from Firebase Storage"""
        try:
            blob = self.bucket.blob(file_path)
            file_bytes = blob.download_as_bytes()
            logger.info(f"File downloaded from {file_path}")
            return file_bytes
        except Exception as e:
            logger.error(f"Error downloading file {file_path}: {e}")
            raise
    
    async def list_files(self, prefix: str) -> list:
        """List all files under a prefix"""
        try:
            blobs = self.bucket.list_blobs(prefix=prefix)
            files = []
            for blob in blobs:
                files.append({
                    'name': blob.name,
                    'size': blob.size,
                    'updated': blob.updated,
                    'public_url': blob.public_url
                })
            logger.info(f"Listed {len(files)} files with prefix {prefix}")
            return files
        except Exception as e:
            logger.error(f"Error listing files with prefix {prefix}: {e}")
            raise

# Global instance
storage_service = FirebaseStorage()

async def get_storage_service() -> FirebaseStorage:
    """Dependency injection for Storage service"""
    return storage_service
