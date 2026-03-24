from .repository import ProductRepository
from .model import ProductModel
from .schema import ProductCreateRequest, ProductUpdateRequest, ProductResponse, ProductListResponse
from ..common.middleware.exception_handlers import APIException, ErrorCode
import logging
from datetime import datetime
from typing import Tuple, List

logger = logging.getLogger(__name__)


class ProductService:
    """Product service - handles business logic for product management"""
    
    def __init__(self, repository: ProductRepository):
        """
        Initialize service with repository
        
        Args:
            repository: ProductRepository instance for database operations
        """
        self.repository = repository
    
    async def create(self, request: ProductCreateRequest) -> ProductResponse:
        """
        Create a new product
        
        Args:
            request: ProductCreateRequest with product details
            
        Returns:
            ProductResponse: Created product details
            
        Raises:
            APIException: If creation fails
        """
        try:
            # Create product model
            product = ProductModel(
                id="",  # Will be set by Firestore
                name=request.name,
                price=request.price,
                category=request.category,
                subcategory=request.subcategory,
                description=request.description,
                detailedDescription=request.detailedDescription,
                features=request.features,
                image=request.image,
                additionalMedia=[m.model_dump() for m in request.additionalMedia] if request.additionalMedia else [],
                technicalSpecs=request.technicalSpecs,
                quantity=request.quantity,
                sku=request.sku,
                is_active=request.is_active,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Save to database
            product_id = await self.repository.create(product)
            product.id = product_id
            
            logger.info(f"Product created with ID: {product_id}")
            
            # Return product response
            return ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                category=product.category,
                subcategory=product.subcategory,
                description=product.description,
                detailedDescription=product.detailedDescription,
                features=product.features,
                image=product.image,
                additionalMedia=product.additionalMedia,
                technicalSpecs=product.technicalSpecs,
                quantity=product.quantity,
                sku=product.sku,
                is_active=product.is_active,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise APIException(
                message="Failed to create product",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
    
    async def update(self, product_id: str, request: ProductUpdateRequest) -> ProductResponse:
        """
        Update product details
        
        Args:
            product_id: Product ID to update
            request: ProductUpdateRequest with updated fields
            
        Returns:
            ProductResponse: Updated product details
            
        Raises:
            APIException: If product not found or update fails
        """
        try:
            # Check if product exists
            existing_product = await self.repository.get_by_id(product_id)
            if not existing_product:
                logger.warning(f"Update attempt for non-existent product: {product_id}")
                raise APIException(
                    message="Product not found",
                    error_code=ErrorCode.RESOURCE_NOT_FOUND,
                    status_code=404
                )
            
            # Build update data only for provided fields
            update_data = {}
            if request.name is not None:
                update_data['name'] = request.name
            if request.description is not None:
                update_data['description'] = request.description
            if request.price is not None:
                update_data['price'] = request.price
            if request.subcategory is not None:
                update_data['subcategory'] = request.subcategory
            if request.detailedDescription is not None:
                update_data['detailedDescription'] = request.detailedDescription
            if request.features is not None:
                update_data['features'] = request.features
            if request.image is not None:
                update_data['image'] = request.image
            if request.additionalMedia is not None:
                update_data['additionalMedia'] = [m.model_dump() for m in request.additionalMedia]
            if request.technicalSpecs is not None:
                update_data['technicalSpecs'] = request.technicalSpecs
            if request.quantity is not None:
                update_data['quantity'] = request.quantity
            if request.sku is not None:
                update_data['sku'] = request.sku
            if request.category is not None:
                update_data['category'] = request.category
            if request.is_active is not None:
                update_data['is_active'] = request.is_active
            
            # Update in database
            await self.repository.update(product_id, update_data)
            
            # Fetch and return updated product
            updated_product = await self.repository.get_by_id(product_id)
            
            logger.info(f"Product {product_id} updated successfully")
            
            return ProductResponse(
                id=updated_product.id,
                name=updated_product.name,
                price=updated_product.price,
                category=updated_product.category,
                subcategory=updated_product.subcategory,
                description=updated_product.description,
                detailedDescription=updated_product.detailedDescription,
                features=updated_product.features,
                image=updated_product.image,
                additionalMedia=updated_product.additionalMedia,
                technicalSpecs=updated_product.technicalSpecs,
                quantity=updated_product.quantity,
                sku=updated_product.sku,
                is_active=updated_product.is_active,
                created_at=updated_product.created_at,
                updated_at=updated_product.updated_at
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            raise APIException(
                message="Failed to update product",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
    
    async def get(self, product_id: str) -> ProductResponse:
        """
        Get single product by ID
        
        Args:
            product_id: Product ID to retrieve
            
        Returns:
            ProductResponse: Product details
            
        Raises:
            APIException: If product not found
        """
        try:
            product = await self.repository.get_by_id(product_id)
            
            if not product:
                logger.warning(f"Get attempt for non-existent product: {product_id}")
                raise APIException(
                    message="Product not found",
                    error_code=ErrorCode.RESOURCE_NOT_FOUND,
                    status_code=404
                )
            
            logger.info(f"Product {product_id} retrieved successfully")
            
            return ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                category=product.category,
                subcategory=product.subcategory,
                description=product.description,
                detailedDescription=product.detailedDescription,
                features=product.features,
                image=product.image,
                additionalMedia=product.additionalMedia,
                technicalSpecs=product.technicalSpecs,
                quantity=product.quantity,
                sku=product.sku,
                is_active=product.is_active,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving product {product_id}: {e}")
            raise APIException(
                message="Failed to retrieve product",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
    
    async def list_products(self, skip: int = 0, limit: int = 10) -> ProductListResponse:
        """
        List all products with pagination
        
        Args:
            skip: Number of products to skip
            limit: Maximum number of products to return
            
        Returns:
            ProductListResponse: Paginated product list
            
        Raises:
            APIException: If listing fails
        """
        try:
            # Validate pagination parameters
            skip = max(0, skip)
            limit = min(100, max(1, limit))  # Max 100 per page
            
            products, total = await self.repository.list_all(skip, limit)
            
            logger.info(f"Listed products: skip={skip}, limit={limit}, total={total}")
            
            product_responses = [
                ProductResponse(
                    id=p.id,
                    name=p.name,
                    price=p.price,
                    category=p.category,
                    subcategory=p.subcategory,
                    description=p.description,
                    detailedDescription=p.detailedDescription,
                    features=p.features,
                    image=p.image,
                    additionalMedia=p.additionalMedia,
                    technicalSpecs=p.technicalSpecs,
                    quantity=p.quantity,
                    sku=p.sku,
                    is_active=p.is_active,
                    created_at=p.created_at,
                    updated_at=p.updated_at
                )
                for p in products
            ]
            
            return ProductListResponse(
                products=product_responses,
                total=total,
                skip=skip,
                limit=limit
            )
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            raise APIException(
                message="Failed to list products",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
    
    async def delete(self, product_id: str) -> bool:
        """
        Delete a product
        
        Args:
            product_id: Product ID to delete
            
        Returns:
            bool: True if successful
            
        Raises:
            APIException: If product not found or deletion fails
        """
        try:
            # Check if product exists
            exists = await self.repository.exists(product_id)
            if not exists:
                logger.warning(f"Delete attempt for non-existent product: {product_id}")
                raise APIException(
                    message="Product not found",
                    error_code=ErrorCode.RESOURCE_NOT_FOUND,
                    status_code=404
                )
            
            # Delete product
            await self.repository.delete(product_id)
            
            logger.info(f"Product {product_id} deleted successfully")
            return True
        
        except APIException:
            raise
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            raise APIException(
                message="Failed to delete product",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=500
            )
