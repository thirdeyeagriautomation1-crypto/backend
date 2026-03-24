from fastapi import APIRouter, Depends, status
from ..common.database.firestore import get_db
from ..common.middleware.base_schema import StandardResponse
from .schema import AdminLoginRequest, AdminSignupRequest, AdminAuthResponse, LoginResponseData
from .service import AuthService
from .repository import AdminRepository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# ============= Dependency Injection =============

def get_admin_repository(db=Depends(get_db)) -> AdminRepository:
    """Inject admin repository with database session"""
    return AdminRepository(db)


def get_auth_service(repository: AdminRepository = Depends(get_admin_repository)) -> AuthService:
    """Inject auth service with repository"""
    return AuthService(repository)


# ============= Routes =============

@router.post(
    "/signup",
    response_model=StandardResponse[AdminAuthResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Admin Signup",
    description="Create a new admin account with email and password"
)
async def admin_signup(
    request: AdminSignupRequest,
    service: AuthService = Depends(get_auth_service)
) -> StandardResponse[AdminAuthResponse]:
    """
    Admin signup endpoint
    
    - Create new admin account
    - Validates email uniqueness
    - Hashes password securely
    - Returns admin details without password
    """
    logger.info(f"Admin signup request for email: {request.email}")
    
    admin = await service.signup(request)
    
    return StandardResponse(
        message="Admin account created successfully",
        data=admin
    )


@router.post(
    "/login",
    response_model=StandardResponse[LoginResponseData],
    status_code=status.HTTP_200_OK,
    summary="Admin Login",
    description="Authenticate admin and get access token"
)
async def admin_login(
    request: AdminLoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> StandardResponse[LoginResponseData]:
    """
    Admin login endpoint
    
    - Authenticate with email and password
    - Returns admin details and auth token
    - Validates admin is active
    """
    logger.info(f"Admin login request for email: {request.email}")
    
    login_data = await service.login(request)
    
    return StandardResponse(
        message="Login successful",
        data=login_data
    )
