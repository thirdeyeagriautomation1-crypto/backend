from datetime import datetime
from typing import Optional, List, Dict, Any


class ProductModel:
    """Product data model representing structure of product collection in database"""
    
    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        price: float = 0.0,
        subcategory: Optional[str] = None,
        description: Optional[str] = None,
        detailedDescription: Optional[str] = None,
        features: Optional[List[str]] = None,
        image: Optional[str] = None,
        additionalMedia: Optional[List[Dict[str, Any]]] = None,
        technicalSpecs: Optional[Dict[str, Any]] = None,
        quantity: int = 0,
        sku: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize Product model
        
        Args:
            id: Unique product identifier
            name: Product name
            price: Product price
            category: Product category
            price: Product price
            subcategory: Optional subcategory
            description: Optional product description
            detailedDescription: Detailed product description
            features: List of product features
            image: Main product image URL
            additionalMedia: Additional media items (videos/images)
            technicalSpecs: Technical specifications
            quantity: Stock quantity
            sku: Stock keeping unit
            is_active: Whether product is active
            created_at: Product creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.subcategory = subcategory
        self.description = description
        self.detailedDescription = detailedDescription
        self.features = features or []
        self.image = image
        self.additionalMedia = additionalMedia or []
        self.technicalSpecs = technicalSpecs or {}
        self.quantity = quantity
        self.sku = sku
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for database storage"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "detailedDescription": self.detailedDescription,
            "features": self.features,
            "image": self.image,
            "additionalMedia": self.additionalMedia,
            "technicalSpecs": self.technicalSpecs,
            "quantity": self.quantity,
            "sku": self.sku,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> "ProductModel":
        """Create model instance from dictionary (database record)"""
        return ProductModel(
            id=data.get("id"),
            name=data.get("name"),
            price=data.get("price", 0.0),
            category=data.get("category"),
            subcategory=data.get("subcategory"),
            description=data.get("description"),
            detailedDescription=data.get("detailedDescription"),
            features=data.get("features", []),
            image=data.get("image"),
            additionalMedia=data.get("additionalMedia", []),
            technicalSpecs=data.get("technicalSpecs", {}),
            quantity=data.get("quantity", 0),
            sku=data.get("sku"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
