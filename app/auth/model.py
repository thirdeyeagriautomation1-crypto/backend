from datetime import datetime
from typing import Optional


class AdminModel:
    """Admin data model representing structure of admin collection in database"""
    
    def __init__(
        self,
        id: str,
        email: str,
        password_hash: str,
        name: str,
        phone: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        """
        Initialize Admin model
        
        Args:
            id: Unique admin identifier
            email: Admin email address
            password_hash: Hashed password
            name: Admin full name
            phone: Optional phone number
            created_at: Account creation timestamp
            updated_at: Last update timestamp
            is_active: Whether admin account is active
        """
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.phone = phone
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for database storage"""
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "name": self.name,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active
        }
    
    @staticmethod
    def from_dict(data: dict) -> "AdminModel":
        """Create model instance from dictionary (database record)"""
        return AdminModel(
            id=data.get("id"),
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            name=data.get("name"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            is_active=data.get("is_active", True)
        )
