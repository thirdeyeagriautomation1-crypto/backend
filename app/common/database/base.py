from datetime import datetime
from typing import Optional, Dict, Any

class FirebaseBaseModel:
    """Base class for Firestore models"""
    
    def __init__(self, **data):
        self.id: Optional[str] = data.get('id')
        self.created_at: datetime = data.get('created_at', datetime.utcnow())
        self.updated_at: datetime = data.get('updated_at', datetime.utcnow())
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for Firestore"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    result[key] = value
                else:
                    result[key] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], doc_id: str = None):
        """Create instance from Firestore document"""
        instance = cls(**data)
        if doc_id:
            instance.id = doc_id
        return instance