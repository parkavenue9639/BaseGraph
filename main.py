"""
FastAPI应用主入口文件
"""
from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="MyGraph API",
    description="基于FastAPI的后端API服务",
    version="0.1.0",
)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "欢迎使用 MyGraph API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

