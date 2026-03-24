from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """
    A standardized response model that includes a message and a data payload.
    """
    message: str = Field(..., description="A message providing context about the response.")
    data: Optional[T] = Field(None, description="The main data payload of the response.")