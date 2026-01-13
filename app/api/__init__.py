"""API路由模块"""
from fastapi import APIRouter
from app.api.endpoints.chat import router as chat_router
from app.api.endpoints.auth import router as auth_router

router = APIRouter()

# 注册各个端点的路由

# chat
router.include_router(chat_router, prefix="/chat", tags=["chat"])

# auth
router.include_router(auth_router, prefix="/auth", tags=["auth"])
