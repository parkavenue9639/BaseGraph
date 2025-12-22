# MyGraph API

基于 FastAPI 和 uv 的后端 API 项目。

## 项目结构

```
MyGraph/
├── app/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           └── items.py      # 示例API端点
├── main.py                    # FastAPI应用入口
├── pyproject.toml            # uv项目配置
└── README.md
```

## 快速开始

### 1. 安装 uv（如果尚未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 运行应用

```bash
uv run uvicorn main:app --reload
```

应用将在 `http://localhost:8000` 启动。

### 4. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 健康检查
- `GET /health` - 健康检查

### 物品管理（示例）
- `GET /api/v1/items/` - 获取所有物品
- `GET /api/v1/items/{item_id}` - 获取指定物品
- `POST /api/v1/items/` - 创建新物品
- `PUT /api/v1/items/{item_id}` - 更新物品
- `DELETE /api/v1/items/{item_id}` - 删除物品

## 开发

### 运行开发服务器（自动重载）

```bash
uv run uvicorn main:app --reload
```

### 添加新依赖

```bash
uv add <package-name>
```

### 添加开发依赖

```bash
uv add --dev <package-name>
```

## 技术栈

- **FastAPI**: 现代、快速的 Web 框架
- **uv**: 快速的 Python 包管理器
- **Uvicorn**: ASGI 服务器

