"""聊天相关 API 端点"""
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sse_starlette.sse import EventSourceResponse
from schema.request.chat import ChatRequest
from service.chat.chat_service import get_chat_service, ChatService

router = APIRouter()


@router.post(
    "/stream",
    summary="流式聊天",
    description="与 AI 进行对话，返回 Server-Sent Events (SSE) 格式的流式响应。支持多轮对话。",
    responses={
        200: {
            "description": "流式响应，返回 SSE 格式的事件流",
            "content": {
                "text/event-stream": {
                    "example": """event: user_message
data: {"role": "user", "content": "你好，你是谁？"}

event: LangGraph
data: {"input": {"messages": [...]}}

event: ChatOpenAI
data: {"chunk": {"type": "AIMessageChunk", "content": "你好！我是..."}}

event: completed
data: {"message": "Stream completed", "event_count": 10}"""
                }
            }
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            }
        }
    },
    tags=["chat"]
)
async def chat_endpoint(
    req: ChatRequest,
    request: Request,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    流式聊天端点，返回 Server-Sent Events (SSE) 格式的响应
    
    **功能说明：**
    - 支持多轮对话，可以传入历史消息
    - 实时流式返回 AI 响应，提供更好的用户体验
    - 自动管理对话状态和上下文
    
    **请求参数说明：**
    - `messages`: 消息列表，每个消息包含：
      - `role`: 角色，可选值：`user`（用户）、`assistant`（AI助手）
      - `content`: 消息内容
    
    **响应格式：**
    返回 SSE (Server-Sent Events) 格式的流式数据，包含以下事件类型：
    - `user_message`: 用户消息确认
    - `LangGraph`: 图执行事件
    - `ChatOpenAI`: AI 响应片段
    - `completed`: 完成事件
    
    **使用 curl 测试：**
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
    
    **多轮对话示例：**
    ```json
    {
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
    }
    ```
    
    **注意事项：**
    - 必须使用 `--no-buffer` 参数以查看实时流式输出
    - Postman 对 SSE 支持有限，建议使用 curl 或浏览器 EventSource API
    """
    try:
        # 从 app.state 获取 graph
        graph = request.app.state.graph
        return await chat_service.chat(req, graph=graph)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))