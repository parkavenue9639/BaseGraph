from fastapi import APIRouter, HTTPException, Depends, Request
from schema.request.chat import ChatRequest
from service.chat.chat_service import get_chat_service, ChatService

router = APIRouter()

@router.post("/stream")
async def chat_endpoint(
    req: ChatRequest,
    request: Request,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    流式聊天端点，返回 Server-Sent Events (SSE) 格式的响应
    
    Example curl request:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/chat/stream" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [
          {
            "role": "user",
            "content": "你好，你是谁？"
          }
        ]
      }' \
      --no-buffer
    ```
    
    Example with multiple messages:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/chat/stream" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [
          {
            "role": "user",
            "content": "你好"
          },
          {
            "role": "assistant",
            "content": "你好！有什么可以帮助你的吗？"
          },
          {
            "role": "user",
            "content": "介绍一下你自己"
          }
        ]
      }' \
      --no-buffer
    ```
    """
    try:
        # 从 app.state 获取 graph
        graph = request.app.state.graph
        return await chat_service.chat(req, graph=graph)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))