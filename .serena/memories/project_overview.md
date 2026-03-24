# Thirdeye API Store Project

## Purpose
Backend API for Thirdeye Courier App managing shipments, tracking, delivery agents, and logistics.

## Tech Stack
- **Framework**: FastAPI (Python 3.x)
- **Databases**: Firestore (Firebase), MySQL (AsyncSQLAlchemy)
- **ORM**: SQLAlchemy (async)
- **Validation**: Pydantic v2
- **Server**: Uvicorn
- **Auth**: Firebase Admin SDK
- **Middleware**: CORS, Exception handlers, Logger, Sanitizer

## Project Structure
```
app/
├── main.py (FastAPI app setup, routes)
├── auth/ (admin login/signup)
│   ├── controller.py (route handlers)
│   ├── schema.py (request/response models)
│   ├── service.py (business logic)
│   ├── model.py (data models)
│   ├── repository.py (db queries)
├── product/ (product CRUD)
├── common/
│   ├── config/ (settings)
│   ├── database/ (Firestore, MySQL helpers)
│   ├── middleware/ (exception handlers, logger, schemas)
│   └── utils/
```

## Architecture Layers
1. **Router**: FastAPI route handlers with dependency injection
2. **Service**: Business logic and error handling
3. **Schema**: Pydantic request/response models
4. **Model**: Data collection structures
5. **Repository**: Database interactions and queries

## API Conventions
- Response model: StandardResponse[T] with message + data
- GET APIs: query parameters
- Write APIs (POST/PUT/DELETE): JSON payloads
- DB session injection at router level
