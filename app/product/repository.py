from typing import Optional, List, Tuple
from google.cloud.firestore import Client
from datetime import datetime
from .model import ProductModel
import logging

logger = logging.getLogger(__name__)

PRODUCT_COLLECTION = "products"


class ProductRepository:
    """Product CRUD operations - handles all database interactions"""
    
    def __init__(self, db: Client):
        """
        Initialize repository with database client
        
        Args:
            db: Firestore database client
        """
        self.db = db
        self.collection = db.collection(PRODUCT_COLLECTION)
    
    async def create(self, product: ProductModel) -> str:
        """
        Create a new product record
        
        Args:
            product: ProductModel instance
            
        Returns:
            str: Document ID of created product
            
        Raises:
            Exception: If creation fails
        """
        try:
            _, doc_ref = self.collection.add(product.to_dict())
            logger.info(f"Product created with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise
    
    async def get_by_id(self, product_id: str) -> Optional[ProductModel]:
        """
        Retrieve product by ID
        
        Args:
            product_id: Product document ID
            
        Returns:
            Optional[ProductModel]: Product model or None if not found
        """
        try:
            doc = self.collection.document(product_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return ProductModel.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error retrieving product {product_id}: {e}")
            raise
    
    async def get_by_name(self, name: str) -> Optional[ProductModel]:
        """
        Retrieve product by name
        
        Args:
            name: Product name
            
        Returns:
            Optional[ProductModel]: Product model or None if not found
        """
        try:
            query = self.collection.where("name", "==", name)
            docs = list(query.stream())
            
            if docs:
                data = docs[0].to_dict()
                data['id'] = docs[0].id
                return ProductModel.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error retrieving product by name {name}: {e}")
            raise
    
    async def list_all(self, skip: int = 0, limit: int = 10) -> Tuple[List[ProductModel], int]:
        """
        List products with pagination
        
        Args:
            skip: Number of products to skip
            limit: Maximum number of products to return
            
        Returns:
            Tuple: (list of ProductModel, total count)
        """
        try:
            # Get total count
            all_docs = list(self.collection.stream())
            total = len(all_docs)
            
            # Get paginated results
            docs = all_docs[skip:skip + limit]
            
            products = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(ProductModel.from_dict(data))
            
            return products, total
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            raise
    
    async def list_by_category(
        self, 
        category: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> Tuple[List[ProductModel], int]:
        """
        List products by category with pagination
        
        Args:
            category: Product category
            skip: Number of products to skip
            limit: Maximum number of products to return
            
        Returns:
            Tuple: (list of ProductModel, total count)
        """
        try:
            # Get all docs in category
            query = self.collection.where("category", "==", category)
            all_docs = list(query.stream())
            total = len(all_docs)
            
            # Get paginated results
            docs = all_docs[skip:skip + limit]
            
            products = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(ProductModel.from_dict(data))
            
            return products, total
        except Exception as e:
            logger.error(f"Error listing products by category: {e}")
            raise
    
    async def update(self, product_id: str, update_data: dict) -> bool:
        """
        Update product record
        
        Args:
            product_id: Product document ID
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if successful
            
        Raises:
            Exception: If update fails
        """
        try:
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            self.collection.document(product_id).update(update_data)
            logger.info(f"Product {product_id} updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            raise
    
    async def delete(self, product_id: str) -> bool:
        """
        Delete product record
        
        Args:
            product_id: Product document ID
            
        Returns:
            bool: True if successful
        """
        try:
            self.collection.document(product_id).delete()
            logger.info(f"Product {product_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            raise
    
    async def exists(self, product_id: str) -> bool:
        """
        Check if product exists
        
        Args:
            product_id: Product document ID
            
        Returns:
            bool: True if product exists
        """
        try:
            doc = self.collection.document(product_id).get()
            return doc.exists
        except Exception as e:
            logger.error(f"Error checking product existence: {e}")
            raise
    
    async def search(
        self, 
        field: str, 
        value: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> Tuple[List[ProductModel], int]:
        """
        Search products by field value
        
        Args:
            field: Field name to search in
            value: Value to search for
            skip: Number of products to skip
            limit: Maximum number of products to return
            
        Returns:
            Tuple: (list of ProductModel, total count)
        """
        try:
            query = self.collection.where(field, "==", value)
            all_docs = list(query.stream())
            total = len(all_docs)
            
            docs = all_docs[skip:skip + limit]
            
            products = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                products.append(ProductModel.from_dict(data))
            
            return products, total
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise
