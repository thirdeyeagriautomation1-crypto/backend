# Implementation Plan

## Tasks
1. ✅ Onboarding complete
2. Implement Auth APIs (admin login, signup)
   - Schema: Auth request/response models
   - Model: Admin data structure
   - Repository: CRUD for admin
   - Service: Auth logic
   - Controller: Route handlers
3. Implement Product APIs (create, update, view, list, delete)
   - Schema: Product request/response models
   - Model: Product data structure
   - Repository: CRUD for products
   - Service: Product logic
   - Controller: Route handlers
4. Create router files with dependency injection
5. Update main.py with new routes

## API Endpoints
### Auth
- POST /apistore/auth/login (admin)
- POST /apistore/auth/signup (admin)

### Product
- POST /apistore/product/create
- PUT /apistore/product/update/{id}
- GET /apistore/product/view?id=xxx
- GET /apistore/product/list?skip=0&limit=10
- DELETE /apistore/product/delete?id=xxx
