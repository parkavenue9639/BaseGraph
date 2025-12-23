"""API路由模块"""
from fastapi import APIRouter
from app.api.endpoints.chat import router as chat_router

router = APIRouter()

# 注册各个端点的路由

# chat
router.include_router(chat_router, prefix="/chat", tags=["chat"])

