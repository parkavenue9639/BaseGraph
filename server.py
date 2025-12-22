"""
使用 uvicorn 启动 FastAPI 应用的服务器入口文件
"""
import uvicorn
from main import app

if __name__ == "__main__":
    # 开发环境配置
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发时自动重载
        log_level="info",
    )

