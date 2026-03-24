# API Documentation - Thirdeye Courier API Store

## Auto-Generated API Structure Implementation

This document outlines the complete implementation of Auth and Product APIs using a proper layered architecture.

---

## Architecture Layers

### 1. **Router Layer** (`controller.py`)
- **Purpose**: Handle HTTP endpoints and dependency injection
- **Responsibility**: Route mapping, request reception, response formatting
- **Features**:
  - FastAPI route handlers
  - Dependency injection for service layer
  - Request validation (via Pydantic schemas)
  - Response wrapping in `StandardResponse`
  - Logging

### 2. **Service Layer** (`service.py`)
- **Purpose**: Business logic and error handling
- **Responsibility**: Processing requests, validation, orchestration
- **Features**:
  - All business logic
  - Error handling with `APIException`
  - Data transformation
  - Transaction management logic
  - Comprehensive logging

### 3. **Schema Layer** (`schema.py`)
- **Purpose**: Request and response data validation
- **Responsibility**: Define API contracts
- **Features**:
  - Pydantic models for requests
  - Pydantic models for responses
  - Field validation rules
  - API documentation examples

### 4. **Model Layer** (`model.py`)
- **Purpose**: Data structure definitions
- **Responsibility**: Represent collection documents
- **Features**:
  - Python classes matching database collections
  - `to_dict()` for database storage
  - `from_dict()` for model instantiation
  - Type hints for clarity

### 5. **Repository Layer** (`repository.py`)
- **Purpose**: Database operations (CRUD)
- **Responsibility**: All database interactions
- **Features**:
  - Create, Read, Update, Delete operations
  - Query building
  - Error handling for DB operations
  - Data access abstraction

---

## API Endpoints

### **Authentication APIs**

#### 1. Admin Signup
```
POST /apistore/auth/signup
Content-Type: application/json

Request Body:
{
  "email": "admin@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "name": "John Admin",
  "phone": "+91-9876543210"
}

Response (201 Created):
{
  "message": "Admin account created successfully",
  "data": {
    "id": "admin_123",
    "email": "admin@example.com",
    "name": "John Admin",
    "phone": "+91-9876543210",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 2. Admin Login
```
POST /apistore/auth/login
Content-Type: application/json

Request Body:
{
  "email": "admin@example.com",
  "password": "password123"
}

Response (200 OK):
{
  "message": "Login successful",
  "data": {
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
```

---

### **Product APIs**

#### 1. Create Product
```
POST /apistore/product/create
Content-Type: application/json

Request Body:
{
  "name": "Organic Wheat Flour",
  "description": "Premium quality wheat flour",
  "price": 250.00,
  "quantity": 100,
  "sku": "FLOUR-001",
  "category": "Grains",
  "is_active": true
}

Response (201 Created):
{
  "message": "Product created successfully",
  "data": {
    "id": "prod_abc123",
    "name": "Organic Wheat Flour",
    "description": "Premium quality wheat flour",
    "price": 250.00,
    "quantity": 100,
    "sku": "FLOUR-001",
    "category": "Grains",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 2. View Single Product
```
GET /apistore/product/view?id=prod_abc123

Response (200 OK):
{
  "message": "Product retrieved successfully",
  "data": {
    "id": "prod_abc123",
    "name": "Organic Wheat Flour",
    "description": "Premium quality wheat flour",
    "price": 250.00,
    "quantity": 100,
    "sku": "FLOUR-001",
    "category": "Grains",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 3. List Products (Paginated)
```
GET /apistore/product/list?skip=0&limit=10

Query Parameters:
- skip: Number of products to skip (default: 0)
- limit: Maximum products to return (default: 10, max: 100)

Response (200 OK):
{
  "message": "Products retrieved successfully",
  "data": {
    "products": [
      {
        "id": "prod_abc123",
        "name": "Organic Wheat Flour",
        "price": 250.00,
        "quantity": 100,
        "category": "Grains",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
      },
      {
        "id": "prod_xyz789",
        "name": "Basmati Rice",
        "price": 400.00,
        "quantity": 50,
        "category": "Grains",
        "is_active": true,
        "created_at": "2024-01-15T11:00:00",
        "updated_at": "2024-01-15T11:00:00"
      }
    ],
    "total": 25,
    "skip": 0,
    "limit": 10
  }
}
```

#### 4. Update Product
```
PUT /apistore/product/update/{product_id}
Content-Type: application/json

Path Parameter:
- product_id: ID of product to update

Request Body (all fields optional):
{
  "name": "Organic Wheat Flour - Premium",
  "price": 280.00,
  "quantity": 150
}

Response (200 OK):
{
  "message": "Product updated successfully",
  "data": {
    "id": "prod_abc123",
    "name": "Organic Wheat Flour - Premium",
    "description": "Premium quality wheat flour",
    "price": 280.00,
    "quantity": 150,
    "sku": "FLOUR-001",
    "category": "Grains",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:45:00"
  }
}
```

#### 5. Delete Product
```
DELETE /apistore/product/delete?id=prod_abc123

Query Parameters:
- id: Product ID to delete

Response (200 OK):
{
  "message": "Product deleted successfully",
  "data": {
    "id": "prod_abc123"
  }
}
```

---

## Error Handling

All API errors follow a standardized format:

```json
{
  "message": "Human-readable error message",
  "error_code": "ERROR_CODE_ENUM",
  "detail": {
    "additional": "error details"
  }
}
```

### Error Codes

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `UNAUTHORIZED` | 401 | Invalid credentials or not authenticated |
| `FORBIDDEN` | 403 | Authenticated but not authorized |
| `NOT_FOUND` | 404 | Resource not found |
| `EMAIL_ALREADY_EXISTS` | 409 | Email already registered |
| `INVALID_INPUT` | 400 | Invalid request data |
| `RESOURCE_NOT_FOUND` | 404 | Product/Resource not found |
| `DUPLICATE_RESOURCE` | 409 | Duplicate resource |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |
| `DATABASE_ERROR` | 500 | Database operation failed |

---

## File Structure

```
app/
├── auth/
│   ├── __init__.py
│   ├── controller.py          # Route handlers
│   ├── schema.py              # Request/Response models
│   ├── service.py             # Business logic
│   ├── model.py               # Data models
│   └── repository.py          # Database CRUD
│
├── product/
│   ├── __init__.py
│   ├── controller.py          # Route handlers
│   ├── schema.py              # Request/Response models
│   ├── service.py             # Business logic
│   ├── model.py               # Data models
│   └── repository.py          # Database CRUD
│
├── common/
│   ├── middleware/
│   │   ├── exception_handlers.py  # Custom exceptions (APIException, ErrorCode)
│   │   ├── base_schema.py         # StandardResponse model
│   │   └── ...
│   ├── database/
│   │   ├── firestore.py           # Firebase database helper
│   │   └── ...
│   └── ...
│
└── main.py                    # FastAPI app setup, router registration
```

---

## Key Design Patterns

### 1. **Dependency Injection**
```python
# In controller.py
def get_repository(db=Depends(get_db)) -> Repository:
    return Repository(db)

def get_service(repo: Repository = Depends(get_repository)) -> Service:
    return Service(repo)

@router.get("/endpoint")
async def endpoint(service: Service = Depends(get_service)):
    # service is automatically injected
    pass
```

### 2. **Clean Service Layer**
```python
# Service contains all business logic
class Service:
    async def create(request: Request) -> Response:
        # Validation logic
        # Business logic
        # Error handling
        # Return response
```

### 3. **Error Handling Pattern**
```python
try:
    # Operation
except APIException:
    raise  # Re-raise custom exceptions
except Exception as e:
    logger.error(f"Error: {e}")
    raise APIException(
        message="User-friendly message",
        error_code=ErrorCode.XXX,
        status_code=500
    )
```

### 4. **Standard Response Format**
```python
class StandardResponse(BaseModel, Generic[T]):
    message: str          # Success/Error message
    data: Optional[T]     # Response payload
```

---

## How to Use

### 1. **Running the Application**
```bash
cd d:/2025/testiclones/thirdeye_apistore
python -m uvicorn app.main:app --reload
```

### 2. **API Documentation (Interactive)**
Once the app is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. **Using the APIs**

#### Example: Create Admin and Login
```bash
# Signup
curl -X POST "http://localhost:8000/apistore/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Test@123",
    "confirm_password": "Test@123",
    "name": "Test Admin",
    "phone": "+91-9876543210"
  }'

# Login
curl -X POST "http://localhost:8000/apistore/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Test@123"
  }'
```

#### Example: Product CRUD
```bash
# Create Product
curl -X POST "http://localhost:8000/apistore/product/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "price": 100.00,
    "quantity": 10,
    "category": "Test"
  }'

# List Products
curl "http://localhost:8000/apistore/product/list?skip=0&limit=10"

# View Product
curl "http://localhost:8000/apistore/product/view?id=prod_id"

# Update Product
curl -X PUT "http://localhost:8000/apistore/product/update/prod_id" \
  -H "Content-Type: application/json" \
  -d '{"price": 150.00}'

# Delete Product
curl -X DELETE "http://localhost:8000/apistore/product/delete?id=prod_id"
```

---

## Best Practices Implemented

✅ **Separation of Concerns** - Each layer has a single responsibility
✅ **Dependency Injection** - Loose coupling between layers
✅ **Error Handling** - Centralized exception handling with standardized format
✅ **Logging** - Comprehensive logging throughout
✅ **Type Hints** - Full type annotations for clarity
✅ **Documentation** - Docstrings on all functions and classes
✅ **Validation** - Request validation via Pydantic
✅ **API Documentation** - Interactive docs via Swagger/ReDoc
✅ **Pagination** - Efficient list endpoints with pagination
✅ **Query Parameters** - GET requests use query parameters
✅ **Request Bodies** - POST/PUT/DELETE use JSON payloads

---

## Next Steps

1. Add authentication middleware to verify tokens for protected endpoints
2. Add database indexes for frequently queried fields
3. Implement caching for read-heavy endpoints
4. Add rate limiting
5. Implement full request/response logging
6. Add unit and integration tests
7. Deploy to production environment

---

## Support

For any issues or questions:
1. Check the error_code and error message in the response
2. Review the server logs
3. Verify request payload matches the schema documentation
4. Check the interactive API docs at `/docs`
