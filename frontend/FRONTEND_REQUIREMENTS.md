# 前端开发需求文档

## 项目概述

开发一个类似 ChatGPT 的聊天界面前端应用，用于调用 MyGraph 后端 API 服务。支持用户注册/登录、实时流式对话等功能。

**后端 API 地址：** `http://localhost:8000`  
**API 文档：** `http://localhost:8000/docs`

---

## 一、技术栈选型

### 推荐方案：React + TypeScript + Vite

#### 1.1 核心框架
- **React 18+** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具（快速开发体验）

#### 1.2 UI 框架
- **Tailwind CSS** - 实用优先的 CSS 框架（推荐）
- 或 **Ant Design** / **Material-UI** - 组件库（可选）

#### 1.3 状态管理
- **Zustand** - 轻量级状态管理（推荐）
- 或 **Redux Toolkit** - 如果需要更复杂的状态管理

#### 1.4 HTTP 客户端
- **Axios** - HTTP 请求库
- **EventSource API** - SSE 流式数据接收（浏览器原生）

#### 1.5 路由
- **React Router v6** - 页面路由

#### 1.6 其他工具
- **React Hook Form** - 表单处理
- **Zod** - 表单验证（可选）
- **date-fns** - 日期格式化
- **clsx** - className 条件拼接

### 备选方案：Vue 3 + TypeScript + Vite

如果团队更熟悉 Vue：
- **Vue 3** + **Composition API**
- **Pinia** - 状态管理
- **Vue Router** - 路由
- **Axios** - HTTP 请求
- **Tailwind CSS** - 样式

---

## 二、UI/UX 设计

### 2.1 整体布局（参考 ChatGPT）

```
┌─────────────────────────────────────────┐
│  Header (Logo + 用户信息 + 登出)        │
├─────────────────────────────────────────┤
│                                          │
│  聊天消息列表区域（可滚动）              │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │ User: 你好                        │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ AI: 你好！有什么可以帮助你的吗？   │  │
│  └───────────────────────────────────┘  │
│                                          │
├─────────────────────────────────────────┤
│  [输入框] [发送按钮] [清空对话]          │
└─────────────────────────────────────────┘
```

### 2.2 页面结构

#### 2.2.1 登录/注册页面
- 简洁的表单设计
- 邮箱 + 密码输入
- 用户名可选（注册时）
- 登录/注册切换
- 错误提示显示

#### 2.2.2 主聊天页面
- **顶部导航栏**
  - 左侧：Logo / 应用名称
  - 右侧：用户头像/名称 + 登出按钮
  
- **消息列表区域**
  - 用户消息：右侧对齐，浅色背景
  - AI 消息：左侧对齐，深色背景
  - 流式输出时显示打字动画效果
  - 自动滚动到最新消息
  
- **输入区域**
  - 多行文本输入框（支持 Enter 发送，Shift+Enter 换行）
  - 发送按钮
  - 清空对话按钮
  - 禁用状态（发送中）

### 2.3 颜色方案（参考 ChatGPT）

```css
/* 浅色主题 */
--bg-primary: #ffffff;
--bg-secondary: #f7f7f8;
--text-primary: #353740;
--text-secondary: #6e6e80;
--border: #e5e5e6;
--user-message-bg: #f7f7f8;
--ai-message-bg: #ffffff;
--button-primary: #10a37f;
--button-hover: #0d8f6e;

/* 深色主题（可选） */
--bg-primary-dark: #343541;
--bg-secondary-dark: #444654;
--text-primary-dark: #ececf1;
--text-secondary-dark: #c5c5d2;
```

---

## 三、功能需求

### 3.1 用户认证功能

#### 3.1.1 用户注册
- [ ] 邮箱输入（必填，格式验证）
- [ ] 密码输入（必填，最少6位）
- [ ] 用户名输入（可选）
- [ ] 表单验证和错误提示
- [ ] 注册成功后自动登录

#### 3.1.2 用户登录
- [ ] 邮箱 + 密码登录
- [ ] 记住登录状态（localStorage 存储 token）
- [ ] Token 过期处理
- [ ] 错误提示

#### 3.1.3 用户信息
- [ ] 显示当前登录用户信息
- [ ] 登出功能（清除 token）

### 3.2 聊天功能

#### 3.2.1 消息发送
- [ ] 文本输入框
- [ ] 发送按钮
- [ ] Enter 发送，Shift+Enter 换行
- [ ] 发送时禁用输入框和按钮
- [ ] 发送成功后清空输入框

#### 3.2.2 消息接收（SSE 流式）
- [ ] 使用 EventSource API 接收 SSE 流
- [ ] 实时显示 AI 响应（打字效果）
- [ ] 处理不同事件类型：
  - `user_message`: 用户消息确认
  - `ChatOpenAI`: AI 响应片段（主要显示内容）
  - `completed`: 完成事件
- [ ] 错误处理和重连机制

#### 3.2.3 消息历史
- [ ] 维护对话历史（内存中）
- [ ] 多轮对话支持
- [ ] 清空对话功能
- [ ] 消息时间戳显示（可选）

#### 3.2.4 UI 交互
- [ ] 自动滚动到最新消息
- [ ] 加载状态显示
- [ ] 错误状态显示
- [ ] 空状态提示

---

## 四、API 接口调用说明

### 4.1 基础配置

```typescript
// config/api.ts
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 获取 Token（从 localStorage）
const getToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// Axios 实例配置
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：添加 Token
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器：处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token 过期，跳转到登录页
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 4.2 认证接口

#### 4.2.1 用户注册

```typescript
// POST /api/v1/auth/register
interface RegisterRequest {
  name?: string;      // 可选，如果为空则使用邮箱前缀
  email: string;      // 必填，邮箱格式
  password: string;   // 必填，至少6位
}

interface UserResponse {
  id: number;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

// 调用示例
const register = async (data: RegisterRequest): Promise<UserResponse> => {
  const response = await apiClient.post('/auth/register', data);
  return response.data;
};
```

#### 4.2.2 用户登录

```typescript
// POST /api/v1/auth/login
interface LoginRequest {
  email: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;  // "bearer"
  user: UserResponse;
}

// 调用示例
const login = async (data: LoginRequest): Promise<TokenResponse> => {
  const response = await apiClient.post('/auth/login', data);
  // 保存 token
  localStorage.setItem('access_token', response.data.access_token);
  localStorage.setItem('user', JSON.stringify(response.data.user));
  return response.data;
};
```

#### 4.2.3 获取当前用户信息

```typescript
// GET /api/v1/auth/me
// 需要 Bearer Token

const getCurrentUser = async (): Promise<UserResponse> => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};
```

### 4.3 聊天接口（SSE 流式）

#### 4.3.1 发送消息并接收流式响应

```typescript
// POST /api/v1/chat/stream
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatRequest {
  messages: ChatMessage[];
}

// SSE 事件类型
type SSEEventType = 'user_message' | 'LangGraph' | 'ChatOpenAI' | 'completed';

interface SSEEvent {
  event: SSEEventType;
  data: any;
}

// 调用示例（使用 EventSource）
const sendMessage = async (
  messages: ChatMessage[],
  onMessage: (content: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): Promise<void> => {
  const token = getToken();
  if (!token) {
    throw new Error('未登录');
  }

  // 使用 fetch 发送 POST 请求，然后读取 SSE 流
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ messages }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error('无法读取响应流');
  }

  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        onComplete();
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('event: ')) {
          const eventType = line.substring(7).trim();
          // 处理事件类型
        } else if (line.startsWith('data: ')) {
          const data = line.substring(6).trim();
          try {
            const parsed = JSON.parse(data);
            
            // 主要处理 ChatOpenAI 事件中的内容
            if (parsed.chunk?.content) {
              onMessage(parsed.chunk.content);
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }
  } catch (error) {
    onError(error as Error);
  }
};
```

#### 4.3.2 更简单的 SSE 实现（使用 EventSource，但需要 GET 请求）

**注意：** EventSource 只支持 GET 请求，但我们的 API 是 POST。因此需要使用 `fetch` + `ReadableStream` 的方式（如上所示）。

或者，可以创建一个封装函数：

```typescript
// utils/sse.ts
export const createSSEConnection = (
  url: string,
  options: {
    method?: string;
    headers?: Record<string, string>;
    body?: any;
    onMessage: (event: string, data: any) => void;
    onError?: (error: Error) => void;
    onComplete?: () => void;
  }
): () => void => {
  let aborted = false;

  const abort = () => {
    aborted = true;
  };

  (async () => {
    try {
      const response = await fetch(url, {
        method: options.method || 'POST',
        headers: options.headers || {},
        body: options.body ? JSON.stringify(options.body) : undefined,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('无法读取响应流');
      }

      let buffer = '';

      while (!aborted) {
        const { done, value } = await reader.read();
        
        if (done) {
          options.onComplete?.();
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        let currentEvent = '';
        let currentData = '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.substring(7).trim();
          } else if (line.startsWith('data: ')) {
            currentData = line.substring(6).trim();
            
            if (currentEvent && currentData) {
              try {
                const parsed = JSON.parse(currentData);
                options.onMessage(currentEvent, parsed);
              } catch (e) {
                // 忽略解析错误
              }
              
              currentEvent = '';
              currentData = '';
            }
          }
        }
      }
    } catch (error) {
      if (!aborted) {
        options.onError?.(error as Error);
      }
    }
  })();

  return abort;
};
```

---

## 五、项目结构

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/          # 组件
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── chat/
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── MessageList.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Layout.tsx
│   ├── pages/              # 页面
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── ChatPage.tsx
│   ├── hooks/              # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useChat.ts
│   │   └── useSSE.ts
│   ├── services/           # API 服务
│   │   ├── api.ts          # Axios 配置
│   │   ├── auth.ts         # 认证 API
│   │   └── chat.ts         # 聊天 API
│   ├── store/              # 状态管理
│   │   ├── authStore.ts
│   │   └── chatStore.ts
│   ├── types/              # TypeScript 类型
│   │   ├── auth.ts
│   │   └── chat.ts
│   ├── utils/              # 工具函数
│   │   ├── sse.ts          # SSE 工具
│   │   └── constants.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env                    # 环境变量
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js      # 如果使用 Tailwind
```

---

## 六、开发步骤

### 6.1 项目初始化

```bash
# 使用 Vite 创建 React + TypeScript 项目
npm create vite@latest frontend -- --template react-ts

cd frontend

# 安装依赖
npm install

# 安装额外依赖
npm install axios zustand react-router-dom
npm install -D tailwindcss postcss autoprefixer
npm install -D @types/node

# 初始化 Tailwind CSS
npx tailwindcss init -p
```

### 6.2 环境变量配置

创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 6.3 核心功能实现顺序

1. **项目基础配置**
   - [ ] 配置 Vite
   - [ ] 配置 Tailwind CSS
   - [ ] 配置 React Router
   - [ ] 配置 Axios

2. **认证功能**
   - [ ] 实现登录页面
   - [ ] 实现注册页面
   - [ ] 实现认证状态管理
   - [ ] 实现路由守卫

3. **聊天功能**
   - [ ] 实现 SSE 连接工具
   - [ ] 实现消息列表组件
   - [ ] 实现输入框组件
   - [ ] 实现聊天页面
   - [ ] 实现流式输出效果

4. **UI 优化**
   - [ ] 响应式布局
   - [ ] 加载状态
   - [ ] 错误处理
   - [ ] 动画效果

---

## 七、关键代码示例

### 7.1 认证 Store (Zustand)

```typescript
// store/authStore.ts
import { create } from 'zustand';
import { UserResponse } from '../types/auth';
import { login, register, getCurrentUser } from '../services/auth';

interface AuthState {
  user: UserResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string | undefined, email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  login: async (email: string, password: string) => {
    const response = await login({ email, password });
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('user', JSON.stringify(response.user));
    set({ user: response.user, token: response.access_token, isAuthenticated: true });
  },

  register: async (name: string | undefined, email: string, password: string) => {
    const response = await register({ name, email, password });
    // 注册成功后自动登录
    await useAuthStore.getState().login(email, password);
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const user = await getCurrentUser();
        set({ user, token, isAuthenticated: true });
      } catch (error) {
        useAuthStore.getState().logout();
      }
    }
  },
}));
```

### 7.2 聊天 Store

```typescript
// store/chatStore.ts
import { create } from 'zustand';
import { ChatMessage } from '../types/chat';
import { sendMessage } from '../services/chat';

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  addMessage: (message: ChatMessage) => void;
  appendToLastMessage: (content: string) => void;
  clearMessages: () => void;
  sendChatMessage: (content: string) => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,

  addMessage: (message: ChatMessage) => {
    set((state) => ({ messages: [...state.messages, message] }));
  },

  appendToLastMessage: (content: string) => {
    set((state) => {
      const messages = [...state.messages];
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.role === 'assistant') {
        lastMessage.content += content;
      } else {
        messages.push({ role: 'assistant', content });
      }
      return { messages };
    });
  },

  clearMessages: () => {
    set({ messages: [], error: null });
  },

  sendChatMessage: async (content: string) => {
    const { messages, addMessage, appendToLastMessage } = get();
    
    // 添加用户消息
    const userMessage: ChatMessage = { role: 'user', content };
    addMessage(userMessage);

    // 添加空的 AI 消息占位
    addMessage({ role: 'assistant', content: '' });

    set({ isLoading: true, error: null });

    try {
      await sendMessage(
        [...messages, userMessage],
        (chunk) => {
          appendToLastMessage(chunk);
        },
        () => {
          set({ isLoading: false });
        },
        (error) => {
          set({ isLoading: false, error: error.message });
        }
      );
    } catch (error) {
      set({ isLoading: false, error: (error as Error).message });
    }
  },
}));
```

### 7.3 聊天页面组件

```typescript
// pages/ChatPage.tsx
import { useEffect, useRef } from 'react';
import { useChatStore } from '../store/chatStore';
import { useAuthStore } from '../store/authStore';
import MessageList from '../components/chat/MessageList';
import ChatInput from '../components/chat/ChatInput';
import Header from '../components/layout/Header';

export default function ChatPage() {
  const { messages, isLoading, sendChatMessage, clearMessages } = useChatStore();
  const { user, logout } = useAuthStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (content: string) => {
    await sendChatMessage(content);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header user={user} onLogout={logout} />
      
      <div className="flex-1 overflow-y-auto p-4">
        <MessageList messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>

      <ChatInput 
        onSend={handleSend} 
        onClear={clearMessages}
        disabled={isLoading}
      />
    </div>
  );
}
```

---

## 八、注意事项

### 8.1 CORS 配置

确保后端已配置 CORS，允许前端域名访问：

```python
# 在 main.py 中添加
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8.2 Token 管理

- Token 存储在 `localStorage`
- Token 过期时间：30 天（后端配置）
- 401 错误时自动跳转登录页

### 8.3 SSE 连接管理

- 确保在组件卸载时关闭 SSE 连接
- 处理网络错误和重连逻辑
- 避免内存泄漏

### 8.4 性能优化

- 使用 `React.memo` 优化消息列表渲染
- 虚拟滚动（如果消息数量很大）
- 防抖处理输入

---

## 九、测试建议

### 9.1 功能测试
- [ ] 用户注册流程
- [ ] 用户登录流程
- [ ] Token 过期处理
- [ ] 消息发送和接收
- [ ] 流式输出效果
- [ ] 多轮对话
- [ ] 清空对话
- [ ] 错误处理

### 9.2 UI 测试
- [ ] 响应式布局（移动端/桌面端）
- [ ] 加载状态显示
- [ ] 错误提示显示
- [ ] 滚动行为

---

## 十、部署建议

### 10.1 开发环境
- 前端：`http://localhost:5173` (Vite 默认)
- 后端：`http://localhost:8000`

### 10.2 生产环境
- 使用 Nginx 反向代理
- 前端构建：`npm run build`
- 静态文件服务
- API 代理配置

---

## 十一、参考资源

- [React 官方文档](https://react.dev/)
- [Vite 文档](https://vitejs.dev/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [Zustand 文档](https://zustand-demo.pmnd.rs/)
- [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)

---

## 十二、开发时间估算

- **项目搭建和配置**：0.5 天
- **认证功能**：1 天
- **聊天功能（SSE）**：2 天
- **UI 优化**：1 天
- **测试和调试**：0.5 天

**总计：约 5 个工作日**

---

**文档版本：** v1.0  
**最后更新：** 2024-01-13
