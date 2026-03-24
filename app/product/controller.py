from fastapi import APIRouter, Depends, status, Query
from ..common.database.firestore import get_db
from ..common.middleware.base_schema import StandardResponse
from .schema import (
    ProductCreateRequest, 
    ProductUpdateRequest, 
    ProductResponse,
    ProductListResponse
)
from .service import ProductService
from .repository import ProductRepository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# ============= Dependency Injection =============

def get_product_repository(db=Depends(get_db)) -> ProductRepository:
    """Inject product repository with database session"""
    return ProductRepository(db)


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    """Inject product service with repository"""
    return ProductService(repository)


# ============= Routes =============

@router.post(
    "/create",
    response_model=StandardResponse[ProductResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Product",
    description="Create a new product with details"
)
async def create_product(
    request: ProductCreateRequest,
    service: ProductService = Depends(get_product_service)
) -> StandardResponse[ProductResponse]:
    """
    Create new product endpoint
    
    - Accepts product details in request body
    - Stores in database
    - Returns created product with ID
    """
    logger.info(f"Create product request for: {request.name}")
    
    product = await service.create(request)
    
    return StandardResponse(
        message="Product created successfully",
        data=product
    )


@router.put(
    "/update/{product_id}",
    response_model=StandardResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Update Product",
    description="Update an existing product"
)
async def update_product(
    product_id: str,
    request: ProductUpdateRequest,
    service: ProductService = Depends(get_product_service)
) -> StandardResponse[ProductResponse]:
    """
    Update product endpoint
    
    - Path parameter: product_id
    - Request body: fields to update (optional fields, update only what's provided)
    - Returns updated product details
    """
    logger.info(f"Update product request for: {product_id}")
    
    product = await service.update(product_id, request)
    
    return StandardResponse(
        message="Product updated successfully",
        data=product
    )


@router.get(
    "/view",
    response_model=StandardResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="View Product",
    description="Get a single product by ID"
)
async def view_product(
    id: str = Query(..., description="Product ID to retrieve"),
    service: ProductService = Depends(get_product_service)
) -> StandardResponse[ProductResponse]:
    """
    Get product by ID endpoint
    
    - Query parameter: id
    - Returns product details
    """
    logger.info(f"View product request for: {id}")
    
    product = await service.get(id)
    
    return StandardResponse(
        message="Product retrieved successfully",
        data=product
    )


@router.get(
    "/list",
    response_model=StandardResponse[ProductListResponse],
    status_code=status.HTTP_200_OK,
    summary="List Products",
    description="Get paginated list of all products"
)
async def list_products(
    skip: int = Query(default=0, ge=0, description="Number of products to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum products to return"),
    service: ProductService = Depends(get_product_service)
) -> StandardResponse[ProductListResponse]:
    """
    List products endpoint
    
    - Query parameters: skip (default 0), limit (default 10, max 100)
    - Returns paginated product list with total count
    """
    logger.info(f"List products request: skip={skip}, limit={limit}")
    
    products = await service.list_products(skip, limit)
    
    return StandardResponse(
        message="Products retrieved successfully",
        data=products
    )


@router.delete(
    "/delete",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Delete Product",
    description="Delete a product by ID"
)
async def delete_product(
    id: str = Query(..., description="Product ID to delete"),
    service: ProductService = Depends(get_product_service)
) -> StandardResponse[dict]:
    """
    Delete product endpoint
    
    - Query parameter: id
    - Removes product from database
    - Returns success message
    """
    logger.info(f"Delete product request for: {id}")
    
    await service.delete(id)
    
    return StandardResponse(
        message="Product deleted successfully",
        data={"id": id}
    )
