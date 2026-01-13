"""
FastAPI应用主入口文件
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from graph.maingraph.MainGraph import MainGraphBuilder
from db.database import get_db

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


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
    
    # 关闭时执行：清理资源
    # 关闭数据库连接池，释放所有连接
    logger.info("Closing database connections...")
    await db.close()
    logger.info("Database connections closed successfully")


app = FastAPI(
    title="MyGraph API",
    description="基于FastAPI的后端API服务",
    version="0.1.0",
    lifespan=lifespan,
)

# 配置 CORS，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 默认端口
        "http://localhost:3000",  # React 默认端口
        "http://localhost:8080",  # Vue 默认端口
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get(
    "/",
    summary="API 根路径",
    description="返回 API 的基本信息和版本号。",
    responses={
        200: {
            "description": "成功",
            "content": {
                "application/json": {
                    "example": {
                        "message": "欢迎使用 MyGraph API",
                        "version": "0.1.0"
                    }
                }
            }
        }
    },
    tags=["系统"]
)
async def root():
    """
    API 根路径
    
    返回 API 的基本欢迎信息和当前版本号。
    """
    return {"message": "欢迎使用 MyGraph API", "version": "0.1.0"}


@app.get(
    "/health",
    summary="健康检查",
    description="检查 API 服务的健康状态，用于监控和负载均衡。",
    responses={
        200: {
            "description": "服务正常",
            "content": {
                "application/json": {
                    "example": {"status": "healthy"}
                }
            }
        }
    },
    tags=["系统"]
)
async def health_check():
    """
    健康检查端点
    
    用于检查 API 服务的运行状态。返回 `{"status": "healthy"}` 表示服务正常运行。
    
    通常用于：
    - 监控系统检查服务可用性
    - 负载均衡器健康检查
    - 容器编排系统的存活探针
    """
    return {"status": "healthy"}

