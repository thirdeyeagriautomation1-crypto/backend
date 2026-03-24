from .repository import AdminRepository
from .model import AdminModel
from .schema import AdminLoginRequest, AdminSignupRequest, AdminAuthResponse, LoginResponseData
from ..common.middleware.exception_handlers import APIException, ErrorCode
import hashlib
import secrets
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash


def generate_token() -> str:
    """Generate a simple auth token"""
    return secrets.token_urlsafe(32)


class AuthService:
    """Auth service - handles business logic for admin authentication"""
    
    def __init__(self, repository: AdminRepository):
        """
        Initialize service with repository
        
        Args:
            repository: AdminRepository instance for database operations
        """
        self.repository = repository
    
    async def signup(self, request: AdminSignupRequest) -> AdminAuthResponse:
        """
        Admin signup - create new admin account
        
        Args:
            request: AdminSignupRequest with email, password, name, phone
            
        Returns:
            AdminAuthResponse: Created admin details
            
        Raises:
            APIException: If email already exists or signup fails
        """
        try:
            # Check if email already exists
            email_exists = await self.repository.email_exists(request.email)
            if email_exists:
                logger.warning(f"Signup attempt with existing email: {request.email}")
                raise APIException(
                    message="Email already registered",
                    error_code=ErrorCode.EMAIL_ALREADY_EXISTS,
                    status_code=409
                )
            
            # Hash password
            password_hash = hash_password(request.password)
            
            # Create admin model
            admin = AdminModel(
                id="",  # Will be set by Firestore
                email=request.email.lower(),
                password_hash=password_hash,
                name=request.name,
                phone=request.phone,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True
            )
            
            # Save to database
            admin_id = await self.repository.create(admin)
            admin.id = admin_id
            
            logger.info(f"Admin signup successful for email: {request.email}")
            
            # Return admin details without password
            return AdminAuthResponse(
                id=admin.id,
                email=admin.email,
                name=admin.name,
                phone=admin.phone,
                created_at=admin.created_at,
                updated_at=admin.updated_at
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Signup error: {e}")
            raise APIException(
                message="Failed to create admin account",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
    
    async def login(self, request: AdminLoginRequest) -> LoginResponseData:
        """
        Admin login - authenticate and return token
        
        Args:
            request: AdminLoginRequest with email and password
            
        Returns:
            LoginResponseData: Admin details and auth token
            
        Raises:
            APIException: If credentials invalid or login fails
        """
        try:
            # Find admin by email
            admin = await self.repository.get_by_email(request.email)
            
            if not admin:
                logger.warning(f"Login attempt with non-existent email: {request.email}")
                raise APIException(
                    message="Invalid email or password",
                    error_code=ErrorCode.UNAUTHORIZED,
                    status_code=401
                )
            
            # Check if admin is active
            if not admin.is_active:
                logger.warning(f"Login attempt with inactive admin: {request.email}")
                raise APIException(
                    message="Admin account is inactive",
                    error_code=ErrorCode.UNAUTHORIZED,
                    status_code=401
                )
            
            # Verify password
            if not verify_password(request.password, admin.password_hash):
                logger.warning(f"Login attempt with wrong password: {request.email}")
                raise APIException(
                    message="Invalid email or password",
                    error_code=ErrorCode.UNAUTHORIZED,
                    status_code=401
                )
            
            # Generate token
            token = generate_token()
            
            logger.info(f"Admin login successful for email: {request.email}")
            
            # Return admin details and token
            admin_response = AdminAuthResponse(
                id=admin.id,
                email=admin.email,
                name=admin.name,
                phone=admin.phone,
                created_at=admin.created_at,
                updated_at=admin.updated_at
            )
            
            return LoginResponseData(
                admin=admin_response,
                token=token
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise APIException(
                message="Login failed",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
