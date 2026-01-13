# MyGraph API

<div align="center">

**基于 FastAPI 和 LangGraph 的智能对话 API 服务**  
**Intelligent Conversation API Service Built with FastAPI and LangGraph**

[English](#english) | [中文](#中文)

</div>

---

## English

### Overview

MyGraph is a modern backend API service built with FastAPI and LangGraph, providing intelligent conversation capabilities with streaming Server-Sent Events (SSE) support. It features a stateful graph-based workflow system with PostgreSQL checkpoint persistence.

### Features

- 🚀 **FastAPI** - Modern, fast web framework
- 📊 **LangGraph** - Stateful, multi-actor applications with LLMs
- 💾 **PostgreSQL** - Persistent checkpoint storage
- 🔄 **Streaming SSE** - Real-time event streaming
- ⚡ **uv** - Fast Python package manager
- 🔌 **Async/Await** - Fully asynchronous architecture

### Project Structure

```
MyGraph/
├── backend/               # Backend API service (this directory)
│   ├── app/               # FastAPI application
│   │   └── api/
│   │       └── endpoints/ # API endpoints
│   │           ├── auth.py
│   │           └── chat.py
│   ├── graph/             # LangGraph workflow definitions
│   │   ├── base/          # Base graph builder and nodes
│   │   └── maingraph/     # Main graph implementation
│   ├── service/           # Business logic services
│   │   ├── chat/          # Chat service
│   │   └── user/          # User service
│   ├── db/                # Database layer
│   │   ├── mysql/         # MySQL models
│   │   └── pg/            # PostgreSQL checkpointer
│   ├── schema/            # Pydantic models
│   │   ├── graph/         # Graph state schemas
│   │   ├── request/       # Request schemas
│   │   └── response/      # Response schemas
│   ├── config/            # Configuration management
│   ├── utils/             # Utility functions
│   ├── main.py            # FastAPI application entry
│   ├── server.py          # Uvicorn server entry
│   └── pyproject.toml     # Project configuration
└── frontend/              # Frontend application (React + TypeScript)
    ├── src/               # Source code
    ├── public/            # Static assets
    └── package.json       # Frontend dependencies
```

### Quick Start

#### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Install Dependencies

Navigate to the backend directory and install dependencies:

```bash
cd backend
uv sync
```

#### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# LLM Configuration
GEMINI_2_5_FLASH_API_KEY=your_api_key_here
GEMINI_2_5_FLASH_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_2_5_FLASH_MODEL=gemini-2.5-flash

# PostgreSQL Configuration
POSTGRES_CONN_STRING=postgresql://user:password@localhost:5432/dbname
```

#### 4. Run the Application

Make sure you're in the `backend/` directory, then run:

```bash
# Using uvicorn directly
uv run uvicorn main:app --reload

# Or using the server script
uv run python server.py
```

The application will start at `http://localhost:8000`.

#### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Health Check
- `GET /health` - Health check endpoint

#### Chat Streaming
- `POST /api/v1/chat/stream` - Stream chat responses using Server-Sent Events (SSE)

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Hello, who are you?"
      }
    ]
  }' \
  --no-buffer \
  -N
```

**Response Format (SSE):**
```
event: user_message
data: {"role": "user", "content": "Hello, who are you?"}

event: LangGraph
data: {"input": {"messages": [...]}}

event: ChatOpenAI
data: {"chunk": {"type": "AIMessageChunk", "content": "Hello! I am..."}}

event: completed
data: {"message": "Stream completed", "event_count": 10}
```

### Development

#### Run Development Server (with auto-reload)

Make sure you're in the `backend/` directory:

```bash
cd backend
uv run uvicorn main:app --reload
```

#### Add New Dependencies

```bash
cd backend
uv add <package-name>
```

#### Add Development Dependencies

```bash
cd backend
uv add --dev <package-name>
```

### Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **LangGraph** - Framework for building stateful, multi-actor applications with LLMs
- **LangChain OpenAI** - Integration with OpenAI-compatible LLMs
- **PostgreSQL** - Relational database for checkpoint persistence
- **SQLAlchemy** - SQL toolkit and ORM
- **uv** - Fast Python package manager
- **Uvicorn** - ASGI server
- **sse-starlette** - Server-Sent Events support
- **psycopg** - PostgreSQL adapter for Python

### Architecture

The application uses LangGraph to create a stateful workflow graph where:
- **Nodes** represent processing steps (e.g., triage, LLM calls)
- **Edges** define the flow between nodes
- **Checkpoints** are persisted to PostgreSQL for conversation state management
- **Events** are streamed in real-time using SSE

---

## 中文

### 项目简介

MyGraph 是一个基于 FastAPI 和 LangGraph 构建的现代后端 API 服务，提供智能对话功能，支持流式 Server-Sent Events (SSE) 输出。采用基于图的状态化工作流系统，并使用 PostgreSQL 进行检查点持久化。

### 核心特性

- 🚀 **FastAPI** - 现代、快速的 Web 框架
- 📊 **LangGraph** - 基于图的状态化多智能体应用
- 💾 **PostgreSQL** - 持久化检查点存储
- 🔄 **流式 SSE** - 实时事件流输出
- ⚡ **uv** - 快速的 Python 包管理器
- 🔌 **异步架构** - 完全异步的设计

### 项目结构

```
MyGraph/
├── backend/               # 后端 API 服务（本目录）
│   ├── app/               # FastAPI 应用
│   │   └── api/
│   │       └── endpoints/ # API 端点
│   │           ├── auth.py
│   │           └── chat.py
│   ├── graph/             # LangGraph 工作流定义
│   │   ├── base/          # 基础图构建器和节点
│   │   └── maingraph/     # 主图实现
│   ├── service/           # 业务逻辑服务
│   │   ├── chat/          # 聊天服务
│   │   └── user/          # 用户服务
│   ├── db/                # 数据库层
│   │   ├── mysql/         # MySQL 模型
│   │   └── pg/            # PostgreSQL 检查点器
│   ├── schema/            # Pydantic 模型
│   │   ├── graph/         # 图状态模式
│   │   ├── request/       # 请求模式
│   │   └── response/      # 响应模式
│   ├── config/            # 配置管理
│   ├── utils/             # 工具函数
│   ├── main.py            # FastAPI 应用入口
│   ├── server.py          # Uvicorn 服务器入口
│   └── pyproject.toml     # 项目配置
└── frontend/              # 前端应用（React + TypeScript）
    ├── src/               # 源代码
    ├── public/            # 静态资源
    └── package.json       # 前端依赖
```

### 快速开始

#### 1. 安装 uv（如果尚未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. 安装依赖

进入 backend 目录并安装依赖：

```bash
cd backend
uv sync
```

#### 3. 配置环境变量

在 `backend/` 目录下创建 `.env` 文件：

```env
# LLM 配置
GEMINI_2_5_FLASH_API_KEY=your_api_key_here
GEMINI_2_5_FLASH_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_2_5_FLASH_MODEL=gemini-2.5-flash

# PostgreSQL 配置
POSTGRES_CONN_STRING=postgresql://user:password@localhost:5432/dbname
```

#### 4. 运行应用

确保在 `backend/` 目录下，然后运行：

```bash
# 直接使用 uvicorn
uv run uvicorn main:app --reload

# 或使用服务器脚本
uv run python server.py
```

应用将在 `http://localhost:8000` 启动。

#### 5. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API 端点

#### 健康检查
- `GET /health` - 健康检查端点

#### 聊天流式接口
- `POST /api/v1/chat/stream` - 使用 Server-Sent Events (SSE) 流式返回聊天响应

**请求示例：**
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
  --no-buffer \
  -N
```

**响应格式 (SSE)：**
```
event: user_message
data: {"role": "user", "content": "你好，你是谁？"}

event: LangGraph
data: {"input": {"messages": [...]}}

event: ChatOpenAI
data: {"chunk": {"type": "AIMessageChunk", "content": "你好！我是..."}}

event: completed
data: {"message": "Stream completed", "event_count": 10}
```

### 开发

#### 运行开发服务器（自动重载）

确保在 `backend/` 目录下：

```bash
cd backend
uv run uvicorn main:app --reload
```

#### 添加新依赖

```bash
cd backend
uv add <package-name>
```

#### 添加开发依赖

```bash
cd backend
uv add --dev <package-name>
```

### 技术栈

- **FastAPI** - 用于构建 API 的现代、快速 Web 框架
- **LangGraph** - 用于构建带 LLM 的状态化多智能体应用框架
- **LangChain OpenAI** - 与 OpenAI 兼容的 LLM 集成
- **PostgreSQL** - 用于检查点持久化的关系型数据库
- **SQLAlchemy** - SQL 工具包和 ORM
- **uv** - 快速的 Python 包管理器
- **Uvicorn** - ASGI 服务器
- **sse-starlette** - Server-Sent Events 支持
- **psycopg** - Python 的 PostgreSQL 适配器

### 架构说明

应用使用 LangGraph 创建状态化工作流图，其中：
- **节点** 表示处理步骤（如分类、LLM 调用）
- **边** 定义节点之间的流程
- **检查点** 持久化到 PostgreSQL 用于对话状态管理
- **事件** 使用 SSE 实时流式输出

### 注意事项

- ⚠️ **Postman 限制**：Postman 对 SSE 流式响应的支持有限，会缓冲所有内容直到连接关闭。建议使用 `curl` 或浏览器 EventSource API 进行测试。
- 📝 **环境变量**：确保在 `backend/` 目录下正确配置 `.env` 文件中的 API 密钥和数据库连接字符串。
- 🔄 **流式输出**：使用 `curl` 测试时，务必添加 `--no-buffer` 和 `-N` 参数以查看实时流式输出。
- 📁 **工作目录**：所有后端相关的命令都需要在 `backend/` 目录下执行。

---

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
