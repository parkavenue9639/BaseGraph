# MyGraph Frontend

基于 React + TypeScript + Vite 构建的聊天应用前端。

## 技术栈

- **React 18+** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **Zustand** - 状态管理
- **React Router** - 路由管理
- **Axios** - HTTP 客户端
- **React Hook Form** - 表单处理

## 快速开始

### 安装依赖

```bash
npm install
```

### 环境变量配置

创建 `.env` 文件（如果不存在）：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:5173` 启动。

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── components/      # 组件
│   │   ├── auth/       # 认证相关组件
│   │   ├── chat/       # 聊天相关组件
│   │   └── layout/     # 布局组件
│   ├── pages/          # 页面
│   ├── hooks/          # 自定义 Hooks
│   ├── services/       # API 服务
│   ├── store/          # 状态管理
│   ├── types/          # TypeScript 类型
│   ├── utils/          # 工具函数
│   ├── App.tsx         # 根组件
│   ├── main.tsx        # 入口文件
│   └── index.css       # 全局样式
├── .env                # 环境变量
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 功能特性

- ✅ 用户注册/登录
- ✅ 实时流式对话（SSE）
- ✅ 消息历史管理
- ✅ 响应式设计
- ✅ Token 认证
- ✅ 路由守卫

## 开发说明

### API 配置

确保后端 API 服务运行在 `http://localhost:8000`，并且已配置 CORS 允许前端域名访问。

### 认证流程

1. 用户注册/登录后，Token 存储在 `localStorage`
2. 所有 API 请求自动携带 Token
3. Token 过期时自动跳转到登录页

### SSE 流式响应

聊天功能使用 Server-Sent Events (SSE) 实现流式响应，支持实时显示 AI 回复。

## 许可证

MIT
