from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# ============= Auth Request Schemas =============

class AdminLoginRequest(BaseModel):
    """Admin login request payload"""
    email: EmailStr = Field(..., description="Admin email")
    password: str = Field(..., min_length=6, description="Admin password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "password123"
            }
        }


class AdminSignupRequest(BaseModel):
    """Admin signup request payload"""
    email: EmailStr = Field(..., description="Admin email")
    password: str = Field(..., min_length=6, description="Admin password")
    confirm_password: str = Field(..., min_length=6, description="Confirm password")
    name: str = Field(..., min_length=2, max_length=100, description="Admin full name")
    phone: Optional[str] = Field(None, description="Admin phone number")
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate that password and confirm_password match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "password123",
                "confirm_password": "password123",
                "name": "John Admin",
                "phone": "+91-9876543210"
            }
        }


# ============= Auth Response Schemas =============

class AdminAuthResponse(BaseModel):
    """Admin authentication response"""
    id: str = Field(..., description="Admin ID")
    email: str = Field(..., description="Admin email")
    name: str = Field(..., description="Admin name")
    phone: Optional[str] = Field(None, description="Admin phone")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "admin_123",
                "email": "admin@example.com",
                "name": "John Admin",
                "phone": "+91-9876543210",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class LoginResponseData(BaseModel):
    """Login response data with token"""
    admin: AdminAuthResponse = Field(..., description="Admin details")
    token: str = Field(..., description="Auth token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "admin": {
                    "id": "admin_123",
                    "email": "admin@example.com",
                    "name": "John Admin",
                    "phone": "+91-9876543210",
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T10:30:00"
                },
                "token": "eyJhbGciOiJIUzI1NiIs..."
            }
        }
