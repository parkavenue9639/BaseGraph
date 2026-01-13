# MyGraph

<div align="center">

**基于 FastAPI 和 LangGraph 的智能对话系统**  
**Intelligent Conversation System Built with FastAPI and LangGraph**

[English](#english) | [中文](#中文)

</div>

---

## English

### Overview

MyGraph is a full-stack intelligent conversation system featuring a modern backend API service built with FastAPI and LangGraph, and a React-based frontend interface. The system provides intelligent conversation capabilities with streaming Server-Sent Events (SSE) support, featuring a stateful graph-based workflow system with PostgreSQL checkpoint persistence.

### Features

- 🚀 **FastAPI** - Modern, fast web framework for backend
- 📊 **LangGraph** - Stateful, multi-actor applications with LLMs
- 💾 **PostgreSQL** - Persistent checkpoint storage
- 🔄 **Streaming SSE** - Real-time event streaming
- ⚡ **uv** - Fast Python package manager
- 🔌 **Async/Await** - Fully asynchronous architecture
- ⚛️ **React + TypeScript** - Modern frontend framework
- 🎨 **Tailwind CSS** - Utility-first CSS framework

### Project Structure

```
MyGraph/
├── backend/               # Backend API service
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
│   ├── config/            # Configuration management
│   ├── utils/             # Utility functions
│   ├── main.py            # FastAPI application entry
│   ├── server.py          # Uvicorn server entry
│   └── pyproject.toml     # Project configuration
└── frontend/              # Frontend application
    ├── src/               # Source code
    │   ├── components/    # React components
    │   ├── pages/         # Page components
    │   ├── services/      # API services
    │   ├── store/         # State management
    │   └── utils/         # Utility functions
    ├── public/            # Static assets
    └── package.json       # Frontend dependencies
```

### Quick Start

#### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (for checkpoint storage)
- MySQL (optional, for user data)

#### Backend Setup

##### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

##### 2. Install Backend Dependencies

```bash
cd backend
uv sync
```

##### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory (you can copy from `.env.example`):

```env
# LLM Configuration
GEMINI_2_5_FLASH_API_KEY=your_api_key_here
GEMINI_2_5_FLASH_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_2_5_FLASH_MODEL=gemini-2.5-flash

# PostgreSQL Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=my_graph
POSTGRES_CONN_STRING=postgresql://user:password@localhost:5432/my_graph

# MySQL Configuration (optional)
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=my_graph
```

##### 4. Run Backend Server

```bash
cd backend
# Using uvicorn directly
uv run uvicorn main:app --reload

# Or using the server script
uv run python server.py
```

The backend API will start at `http://localhost:8000`.

##### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Frontend Setup

##### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

##### 2. Configure Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

##### 3. Run Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:5173`.



### Development

#### Backend Development

```bash
cd backend
# Run with auto-reload
uv run uvicorn main:app --reload

# Add new dependencies
uv add <package-name>

# Add development dependencies
uv add --dev <package-name>
```

#### Frontend Development

```bash
cd frontend
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Technology Stack

#### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangGraph** - Framework for building stateful, multi-actor applications with LLMs
- **LangChain OpenAI** - Integration with OpenAI-compatible LLMs
- **PostgreSQL** - Relational database for checkpoint persistence
- **MySQL** - Relational database for user data
- **SQLAlchemy** - SQL toolkit and ORM
- **uv** - Fast Python package manager
- **Uvicorn** - ASGI server
- **sse-starlette** - Server-Sent Events support
- **psycopg** - PostgreSQL adapter for Python

#### Frontend
- **React 18+** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - State management
- **React Router** - Routing
- **Axios** - HTTP client
- **React Hook Form** - Form handling

### Architecture

The application uses LangGraph to create a stateful workflow graph where:
- **Nodes** represent processing steps (e.g., triage, LLM calls)
- **Edges** define the flow between nodes
- **Checkpoints** are persisted to PostgreSQL for conversation state management
- **Events** are streamed in real-time using SSE

The frontend communicates with the backend through RESTful API and SSE for streaming responses.

### Notes

- ⚠️ **Postman Limitation**: Postman has limited support for SSE streaming responses and will buffer all content until the connection closes. It's recommended to use `curl` or browser EventSource API for testing.
- 📝 **Environment Variables**: Make sure to properly configure API keys and database connection strings in the `.env` files.
- 🔄 **Streaming Output**: When testing with `curl`, make sure to add `--no-buffer` and `-N` flags to see real-time streaming output.
- 📁 **Working Directory**: All backend-related commands need to be executed in the `backend/` directory.

---

## 中文

### 项目简介

MyGraph 是一个全栈智能对话系统，包含基于 FastAPI 和 LangGraph 构建的现代后端 API 服务，以及基于 React 的前端界面。系统提供智能对话功能，支持流式 Server-Sent Events (SSE) 输出，采用基于图的状态化工作流系统，并使用 PostgreSQL 进行检查点持久化。

### 核心特性

- 🚀 **FastAPI** - 现代、快速的 Web 框架（后端）
- 📊 **LangGraph** - 基于图的状态化多智能体应用
- 💾 **PostgreSQL** - 持久化检查点存储
- 🔄 **流式 SSE** - 实时事件流输出
- ⚡ **uv** - 快速的 Python 包管理器
- 🔌 **异步架构** - 完全异步的设计
- ⚛️ **React + TypeScript** - 现代前端框架
- 🎨 **Tailwind CSS** - 实用优先的 CSS 框架

### 项目结构

```
MyGraph/
├── backend/               # 后端 API 服务
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
│   ├── config/            # 配置管理
│   ├── utils/             # 工具函数
│   ├── main.py            # FastAPI 应用入口
│   ├── server.py          # Uvicorn 服务器入口
│   └── pyproject.toml     # 项目配置
└── frontend/              # 前端应用
    ├── src/               # 源代码
    │   ├── components/    # React 组件
    │   ├── pages/         # 页面组件
    │   ├── services/      # API 服务
    │   ├── store/         # 状态管理
    │   └── utils/         # 工具函数
    ├── public/            # 静态资源
    └── package.json       # 前端依赖
```

### 快速开始

#### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL（用于检查点存储）
- MySQL（可选，用于用户数据）

#### 后端设置

##### 1. 安装 uv（如果尚未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

##### 2. 安装后端依赖

```bash
cd backend
uv sync
```

##### 3. 配置环境变量

在 `backend/` 目录下创建 `.env` 文件（可从 `.env.example` 复制）：

```env
# LLM 配置
GEMINI_2_5_FLASH_API_KEY=your_api_key_here
GEMINI_2_5_FLASH_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_2_5_FLASH_MODEL=gemini-2.5-flash

# PostgreSQL 配置
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=my_graph
POSTGRES_CONN_STRING=postgresql://user:password@localhost:5432/my_graph

# MySQL 配置（可选）
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=my_graph
```

##### 4. 运行后端服务器

```bash
cd backend
# 直接使用 uvicorn
uv run uvicorn main:app --reload

# 或使用服务器脚本
uv run python server.py
```

后端 API 将在 `http://localhost:8000` 启动。

##### 5. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 前端设置

##### 1. 安装前端依赖

```bash
cd frontend
npm install
```

##### 2. 配置环境变量

在 `frontend/` 目录下创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

##### 3. 运行前端开发服务器

```bash
cd frontend
npm run dev
```

前端将在 `http://localhost:5173` 启动。

### API 端点

#### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出

#### 健康检查
- `GET /health` - 健康检查端点

#### 聊天流式接口
- `POST /api/v1/chat/stream` - 使用 Server-Sent Events (SSE) 流式返回聊天响应

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
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

#### 后端开发

```bash
cd backend
# 运行开发服务器（自动重载）
uv run uvicorn main:app --reload

# 添加新依赖
uv add <package-name>

# 添加开发依赖
uv add --dev <package-name>
```

#### 前端开发

```bash
cd frontend
# 运行开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 技术栈

#### 后端
- **FastAPI** - 用于构建 API 的现代、快速 Web 框架
- **LangGraph** - 用于构建带 LLM 的状态化多智能体应用框架
- **LangChain OpenAI** - 与 OpenAI 兼容的 LLM 集成
- **PostgreSQL** - 用于检查点持久化的关系型数据库
- **MySQL** - 用于用户数据的关系型数据库
- **SQLAlchemy** - SQL 工具包和 ORM
- **uv** - 快速的 Python 包管理器
- **Uvicorn** - ASGI 服务器
- **sse-starlette** - Server-Sent Events 支持
- **psycopg** - Python 的 PostgreSQL 适配器

#### 前端
- **React 18+** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Zustand** - 状态管理
- **React Router** - 路由管理
- **Axios** - HTTP 客户端
- **React Hook Form** - 表单处理

### 架构说明

应用使用 LangGraph 创建状态化工作流图，其中：
- **节点** 表示处理步骤（如分类、LLM 调用）
- **边** 定义节点之间的流程
- **检查点** 持久化到 PostgreSQL 用于对话状态管理
- **事件** 使用 SSE 实时流式输出

前端通过 RESTful API 和 SSE 与后端通信，实现流式响应。

### 注意事项

- ⚠️ **Postman 限制**：Postman 对 SSE 流式响应的支持有限，会缓冲所有内容直到连接关闭。建议使用 `curl` 或浏览器 EventSource API 进行测试。
- 📝 **环境变量**：确保正确配置 `.env` 文件中的 API 密钥和数据库连接字符串。
- 🔄 **流式输出**：使用 `curl` 测试时，务必添加 `--no-buffer` 和 `-N` 参数以查看实时流式输出。
- 📁 **工作目录**：所有后端相关的命令都需要在 `backend/` 目录下执行。

---

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
