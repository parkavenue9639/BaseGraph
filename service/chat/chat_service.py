import asyncio
from typing import Any, List, AsyncIterator

from fastapi.exceptions import HTTPException
from schema.request.chat import ChatRequest
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages.human import HumanMessage
from sse_starlette.sse import EventSourceResponse

import json
import logging

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self) -> None:
        pass

    async def chat(self, req: ChatRequest, graph: CompiledStateGraph) -> Any:
        try:
            messages = []
            user_message_events = [] # 用户消息事件记录
            # event_index = get_conversation_event_index(db, conversation_id) + 1
            event_index = 0
            event_queue = asyncio.Queue()

            for message in req.messages:
                message_dict = {"role": message.role, "content": message.content}
                message_content = message.content
                messages.append(message_dict)

                # 创建用户消息事件记录
                user_message_events.append(
                    {
                        "event": "user_message",
                        "index": event_index,
                        "data": json.dumps({
                            "role": message.role,
                         "content": message_content
                    }   , ensure_ascii=False)
                    }
                )
                event_index += 1
        
            _task = asyncio.create_task(self.workflow(graph=graph, event_index=event_index, messages=messages, user_message_event=user_message_events, event_queue=event_queue))
            return EventSourceResponse(self.event_generator(event_queue), media_type="text/event-stream", sep="\n")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def workflow(
        self, 
        graph: CompiledStateGraph,
        event_index: int,
        messages: List,
        user_message_event: List,
        event_queue: asyncio.Queue
        ):
        # 存储所有事件消息的列表
        all_events = []
        all_events.extend(user_message_event)
        
        # 先发送用户消息事件
        for event in user_message_event:
            await event_queue.put(event)
        
        try:
            async for event in self.run_agent(graph, user_input_mesages=messages):
                await event_queue.put(event)
        except Exception as e:
            logger.error(f"Workflow error: {e}", exc_info=True)
            await event_queue.put({
                "kind": "end",
                "event": "error",
                "data": str(e)
            })

    async def run_agent(
        self,
        graph: CompiledStateGraph,
        user_input_mesages: List
        ) -> AsyncIterator[dict]:
        try:
            human_messages = []

            if user_input_mesages and len(user_input_mesages) > 0:
                # 添加用户消息至历史
                pass
            
            for message in user_input_mesages:
                human_messages.append(HumanMessage(content=message.get("content", ""), name="user_query"))

            async for event in graph.astream_events({
                "messages": human_messages
            }):
                try:
                    async for handler_result in self.event_handler(event):
                        yield handler_result
                except Exception as e:
                    logger.error(f"Event handler error: {e}", exc_info=True)
                    yield {
                        "kind": "end",
                        "event": "error",
                        "data": str(e)
                    }
                    break
        
        except Exception as e:
            logger.error(f"Run agent error: {e}", exc_info=True)
            yield {
                "kind": "end",
                "event": "error",
                "data": str(e)
            }
    
    async def event_handler(self, event) -> AsyncIterator[dict]:
        try:
            # 解析事件信息
            kind = event.get("event")
            data = event.get("data")
            name = event.get("name")
            logger.info(f"kind: {kind}, data: {data}, name: {name}")

            yield {
                "kind": kind,
                "event": name,
                "data": data
            }

        except Exception as e:
            logger.error(f"Event handler error: {e}", exc_info=True)
            yield {
                "kind": "end",
                "event": "error",
                "data": str(e)
            }

    async def event_generator(self, event_queue: asyncio.Queue) -> AsyncIterator[str]:
        """生成 SSE 格式的事件流"""
        try:
            while True:
                try:
                    # 从队列获取事件，设置超时避免无限等待
                    event = await asyncio.wait_for(event_queue.get(), timeout=1.0)
                    
                    # 格式化 SSE 事件
                    event_str = f"event: {event.get('event', 'message')}\n"
                    data_str = json.dumps(event.get('data', {}), ensure_ascii=False)
                    event_str += f"data: {data_str}\n\n"
                    
                    yield event_str
                    
                    # 如果是结束事件，退出循环
                    if event.get('kind') == 'end':
                        break
                        
                except asyncio.TimeoutError:
                    # 超时检查是否应该继续等待
                    continue
                except Exception as e:
                    logger.error(f"Event generator error: {e}", exc_info=True)
                    error_event = f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
                    yield error_event
                    break
                    
        except asyncio.CancelledError:
            logger.info("Event generator cancelled")
            raise


def get_chat_service():
    return ChatService()