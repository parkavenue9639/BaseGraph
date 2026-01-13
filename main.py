"""
FastAPI应用主入口文件
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import router
from graph.maingraph.MainGraph import MainGraphBuilder
from db.database import get_db

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    # 初始化 MySQL 数据库表
    db = get_db()
    await db.init_tables()
    
    main_graph_builder = MainGraphBuilder()
    app.state.graph = await main_graph_builder.build_graph()
    yield
    # 关闭时执行（如果需要清理资源，在这里添加）


app = FastAPI(
    title="MyGraph API",
    description="基于FastAPI的后端API服务",
    version="0.1.0",
    lifespan=lifespan,
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

