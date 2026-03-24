# Code Style and Conventions

## Python/Pydantic Patterns
- Type hints: Full type annotations on all functions
- Pydantic Models: Inherit from BaseModel, use Field() for descriptions
- Async: Use async/await throughout
- Logging: Use logging module, not print()
- Error Handling: Custom exceptions in exception_handlers.py

## API Response Format
```python
StandardResponse(
    message="Success message",
    data=<result_object>
)
```

## Naming Conventions
- Files: snake_case (controller.py, schema.py)
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

## Firestore/Database
- FirestoreDB helper class for async operations
- SessionLocal for MySQL async sessions
- Dependency injection via get_db() or Depends()
