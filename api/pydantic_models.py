from pydantic import BaseModel, Field
from enum import Enum

class ModelName(str, Enum):
    GPT4O_MINI = "gpt-4o-mini"
    GPT4O = "gpt-4o"
    GPT35_TURBO = "gpt-3.5-turbo"

class UserQuery(BaseModel):
    query: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4O_MINI)

class DeleteFileRequest(BaseModel):
    file_id: int

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
