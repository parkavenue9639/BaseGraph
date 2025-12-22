"""API路由模块"""
from fastapi import APIRouter
from app.api.endpoints import items

router = APIRouter()

# 注册各个端点的路由
router.include_router(items.router, prefix="/items", tags=["items"])

