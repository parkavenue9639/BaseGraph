from pydantic import BaseModel, Field
from typing import List

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender(user or ...)")
    content: str = Field(..., description="The content of the message")


class ChatRequest(BaseModel):
    messages: List[ChatMessage]