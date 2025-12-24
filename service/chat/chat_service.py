import asyncio
import uuid
from typing import Any, List, AsyncIterator

from fastapi.exceptions import HTTPException
from schema.request.chat import ChatRequest
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from langchain_core.messages.human import HumanMessage
from langchain_core.messages import BaseMessage
from sse_starlette.sse import EventSourceResponse

import json
import logging

logger = logging.getLogger(__name__)


class ChatService:

    async def chat(self, req: ChatRequest, graph: CompiledStateGraph) -> Any:
        try:
            # 生成唯一的 thread_id 用于 checkpointer
            thread_id = str(uuid.uuid4())
            
            messages = []
            user_message_events = []
            event_index = 0
            event_queue = asyncio.Queue()
            workflow_done = asyncio.Event()  # 用于标记 workflow 完成，避免 event_generator 无限等待

            for message in req.messages:
                message_dict = {"role": message.role, "content": message.content}
                message_content = message.content
                messages.append(message_dict)

                user_message_events.append(
                    {
                        "event": "user_message",
                        "index": event_index,
                        "data": {
                            "role": message.role,
                            "content": message_content
                        }
                    }
                )
                event_index += 1
        
            # 在后台任务中运行 workflow，同时立即返回 SSE 响应
            _task = asyncio.create_task(self.workflow(
                graph=graph, 
                thread_id=thread_id,
                event_index=event_index, 
                messages=messages, 
                user_message_event=user_message_events, 
                event_queue=event_queue,
                workflow_done=workflow_done
            ))
            return EventSourceResponse(
                self.event_generator(event_queue, workflow_done), 
                media_type="text/event-stream", 
                sep="\n"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def workflow(
        self, 
        graph: CompiledStateGraph,
        thread_id: str,
        event_index: int,
        messages: List,
        user_message_event: List,
        event_queue: asyncio.Queue,
        workflow_done: asyncio.Event
        ):
        try:
            # 先发送用户消息事件，确保客户端能立即看到用户输入
            for event in user_message_event:
                await event_queue.put(event)
                logger.debug(f"Put user message event: {event.get('event')}")
            
            event_count = 0
            async for event in self.run_agent(graph, thread_id=thread_id, user_input_mesages=messages):
                await event_queue.put(event)
                event_count += 1
                logger.debug(f"Put agent event {event_count}: {event.get('event', 'unknown')}")
            
            # 发送完成事件
            await event_queue.put({
                "kind": "end",
                "event": "completed",
                "data": {"message": "Stream completed", "event_count": event_count}
            })
            logger.info(f"Workflow completed, total events: {event_count}")
            # 发送 None 作为结束信号，参考其他项目的实现
            await event_queue.put(None)
        except Exception as e:
            logger.error(f"Workflow error: {e}", exc_info=True)
            await event_queue.put({
                "kind": "end",
                "event": "error",
                "data": str(e)
            })
            # 发送 None 作为结束信号
            await event_queue.put(None)
        finally:
            # 标记 workflow 完成，通知 event_generator 可以安全退出
            workflow_done.set()
            # 确保发送 None 作为结束信号（防止异常情况下没有发送）
            try:
                await event_queue.put(None)
            except:
                pass

    async def run_agent(
        self,
        graph: CompiledStateGraph,
        thread_id: str,
        user_input_mesages: List
        ) -> AsyncIterator[dict]:
        try:
            human_messages = []
            for message in user_input_mesages:
                human_messages.append(HumanMessage(content=message.get("content", ""), name="user_query"))

            # 配置 checkpointer，用于持久化对话状态
            config = {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": ""
                }
            }

            async for event in graph.astream_events(
                {"messages": human_messages},
                version="v2",
                config=config
            ):
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
    
    def _serialize_message(self, msg: Any) -> dict:
        """将消息对象序列化为可 JSON 序列化的字典"""
        if isinstance(msg, BaseMessage):
            return {
                "type": msg.__class__.__name__,
                "content": msg.content,
                "name": getattr(msg, "name", None),
                "id": getattr(msg, "id", None),
            }
        elif isinstance(msg, dict):
            return msg
        elif hasattr(msg, "__dict__"):
            return str(msg)
        else:
            return {"value": str(msg)}
    
    def _serialize_command(self, cmd: Command) -> dict:
        """将 Command 对象序列化为可 JSON 序列化的字典"""
        result = {
            "type": "Command",
        }
        if hasattr(cmd, "goto"):
            goto_value = getattr(cmd, "goto", None)
            result["goto"] = str(goto_value) if goto_value is not None else None
        if hasattr(cmd, "update"):
            update_value = getattr(cmd, "update", None)
            result["update"] = self._serialize_data(update_value) if update_value is not None else None
        if hasattr(cmd, "skip"):
            skip_value = getattr(cmd, "skip", None)
            result["skip"] = skip_value if skip_value is not None else None
        if hasattr(cmd, "__dict__"):
            for key, value in cmd.__dict__.items():
                if key not in result:
                    result[key] = self._serialize_data(value)
        return result
    
    def _serialize_data(self, data: Any) -> Any:
        """递归序列化数据，处理消息对象和 Command 对象"""
        if isinstance(data, BaseMessage):
            return self._serialize_message(data)
        elif isinstance(data, Command):
            return self._serialize_command(data)
        elif isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}
        else:
            return data

    def _is_empty_chunk(self, data: Any) -> bool:
        """检查是否是空 chunk 事件"""
        if not isinstance(data, dict):
            return False
        
        chunk = data.get("chunk")
        if chunk and isinstance(chunk, dict):
            content = chunk.get("content", "")
            if not content or content == "":
                # 即使 content 为空，如果有 tool_calls 或 metadata，仍然是有意义的事件
                has_tool_calls = bool(chunk.get("tool_calls") or chunk.get("tool_call_chunks"))
                has_metadata = bool(chunk.get("response_metadata") or chunk.get("usage_metadata"))
                if not has_tool_calls and not has_metadata:
                    logger.debug(f"Detected empty chunk: content='{content}', has_tool_calls={has_tool_calls}, has_metadata={has_metadata}")
                    return True
        
        return False
    
    async def event_handler(self, event) -> AsyncIterator[dict]:
        try:
            kind = event.get("event")
            data = event.get("data")
            name = event.get("name")
            
            # 过滤空 chunk 事件，减少不必要的网络传输
            if self._is_empty_chunk(data):
                logger.debug(f"Filtered empty chunk event: {name}")
                return
            
            logger.debug(f"Processing event: kind={kind}, name={name}")
            # 序列化数据，确保 BaseMessage 和 Command 对象可以 JSON 序列化
            serialized_data = self._serialize_data(data)

            yield {
                "kind": kind,
                "event": name,
                "data": serialized_data
            }

        except Exception as e:
            logger.error(f"Event handler error: {e}", exc_info=True)
            yield {
                "kind": "end",
                "event": "error",
                "data": str(e)
            }

    async def event_generator(self, event_queue: asyncio.Queue, workflow_done: asyncio.Event) -> AsyncIterator[dict]:
        """生成 SSE 格式的事件流
        
        EventSourceResponse 期望接收字典格式：{"event": "event_name", "data": "json_string"}
        参考其他项目的实现，直接等待队列，不使用超时，确保事件能够流式输出
        """
        try:
            while True:
                event = await event_queue.get()
                
                # 使用 None 作为结束信号，参考其他项目的实现
                if event is None:
                    break
                
                event_name = event.get('event', 'message')
                event_data = event.get('data', {})
                
                # 确保 data 是 JSON 字符串格式
                if isinstance(event_data, str):
                    data_str = event_data
                else:
                    data_str = json.dumps(event_data, ensure_ascii=False)
                
                logger.debug(f"Yielding SSE event: {event_name}")
                yield {
                    "event": event_name,
                    "data": data_str
                }
                
                # 如果事件标记为结束，也退出循环
                if event.get('kind') == 'end':
                    logger.info("Received end event, closing stream")
                    break
                    
        except asyncio.CancelledError:
            logger.info("Event generator cancelled")
            raise
        except Exception as e:
            logger.error(f"Event generator error: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)}, ensure_ascii=False)
            }


def get_chat_service():
    return ChatService()