from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserResponse(BaseModel):
    """用户信息响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
