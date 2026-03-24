from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= Shared Sub-Schemas =============

class MediaItem(BaseModel):
    """Additional media item schema"""
    type: str = Field(..., description="Media type (e.g., video, image)")
    url: str = Field(..., description="Media URL")
    isUrl: bool = Field(default=True, description="Whether it is a URL")


# ============= Product Request Schemas =============

class ProductCreateRequest(BaseModel):
    """Product creation request payload"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    price: float = Field(default=0.0, ge=0, description="Product price")
    subcategory: Optional[str] = Field(None, max_length=100, description="Product subcategory")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    detailedDescription: Optional[str] = Field(None, description="Detailed product description")
    features: Optional[List[str]] = Field(default=[], description="List of product features")
    image: Optional[str] = Field(None, description="Main product image URL")
    additionalMedia: Optional[List[MediaItem]] = Field(default=[], description="Additional media items")
    technicalSpecs: Optional[Dict[str, Any]] = Field(default={}, description="Technical specifications")
    quantity: int = Field(default=0, ge=0, description="Stock quantity")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    is_active: bool = Field(default=True, description="Whether product is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "AgroSmart WiFi Pro Controller",
                "category": "wireless",
                "subcategory": "WiFi Controllers",
                "price": 250.00,
                "description": "Advanced 12-zone smart irrigation controller.",
                "detailedDescription": "The AgroSmart WiFi Pro Controller offers industry-leading capabilities.",
                "features": ["Real-time weather data", "Control from anywhere"],
                "image": "https://images.unsplash.com/photo-1685475188388-2a266e6bd5c4?w=800",
                "additionalMedia": [
                    {
                        "type": "video",
                        "url": "https://www.youtube.com/watch?v=example",
                        "isUrl": True
                    }
                ],
                "technicalSpecs": {
                    "Zones": "12 Base (Expandable to 24)",
                    "Connectivity": "802.11 b/g/n @ 2.4 GHz"
                },
                "quantity": 100,
                "sku": "AGRO-001",
                "is_active": True
            }
        }


class ProductUpdateRequest(BaseModel):
    """Product update request payload"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Product name")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Product category")
    price: Optional[float] = Field(None, ge=0, description="Product price")
    subcategory: Optional[str] = Field(None, max_length=100, description="Product subcategory")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    detailedDescription: Optional[str] = Field(None, description="Detailed product description")
    features: Optional[List[str]] = Field(None, description="List of product features")
    image: Optional[str] = Field(None, description="Main product image URL")
    additionalMedia: Optional[List[MediaItem]] = Field(None, description="Additional media items")
    technicalSpecs: Optional[Dict[str, Any]] = Field(None, description="Technical specifications")
    quantity: Optional[int] = Field(None, ge=0, description="Stock quantity")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    is_active: Optional[bool] = Field(None, description="Whether product is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "AgroSmart WiFi Pro Controller - V2",
                "price": 280.00,
                "quantity": 150
            }
        }


# ============= Product Response Schemas =============

class ProductResponse(BaseModel):
    """Standard product response"""
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    subcategory: Optional[str] = Field(None, description="Product subcategory")
    description: Optional[str] = Field(None, description="Product description")
    detailedDescription: Optional[str] = Field(None, description="Detailed product description")
    features: List[str] = Field(default=[], description="List of product features")
    image: Optional[str] = Field(None, description="Main product image URL")
    additionalMedia: List[MediaItem] = Field(default=[], description="Additional media items")
    technicalSpecs: Dict[str, Any] = Field(default={}, description="Technical specifications")
    quantity: int = Field(..., description="Stock quantity")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    is_active: bool = Field(..., description="Whether product is active")
    created_at: datetime = Field(..., description="Product creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_123",
                "name": "AgroSmart WiFi Pro Controller",
                "category": "wireless",
                "subcategory": "WiFi Controllers",
                "price": 250.00,
                "description": "Advanced 12-zone smart irrigation controller.",
                "detailedDescription": "The AgroSmart WiFi Pro Controller offers industry-leading capabilities.",
                "features": ["Real-time weather data", "Control from anywhere"],
                "image": "https://images.unsplash.com/photo-1685475188388-2a266e6bd5c4?w=800",
                "additionalMedia": [
                    {
                        "type": "video",
                        "url": "https://www.youtube.com/watch?v=example",
                        "isUrl": True
                    }
                ],
                "technicalSpecs": {
                    "Zones": "12 Base (Expandable to 24)"
                },
                "quantity": 100,
                "sku": "AGRO-001",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class ProductListResponse(BaseModel):
    """Paginated product list response"""
    products: List[ProductResponse] = Field(..., description="List of products")
    total: int = Field(..., description="Total product count")
    skip: int = Field(..., description="Number of products skipped")
    limit: int = Field(..., description="Number of products returned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "id": "prod_123",
                        "name": "Organic Wheat Flour",
                        "price": 250.00,
                        "quantity": 100,
                        "category": "Grains",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 50,
                "skip": 0,
                "limit": 10
            }
        }
