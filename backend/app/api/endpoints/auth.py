"""认证相关 API 端点"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from service.user.user_service import get_user_service, UserService
from schema.request.auth import RegisterRequest, LoginRequest
from schema.response.auth import UserResponse, TokenResponse

router = APIRouter()

# OAuth2 密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """获取当前登录用户（依赖注入）
    
    Args:
        token: JWT token
        user_service: 用户服务实例
        
    Returns:
        当前用户信息
    """
    return await user_service.get_current_user_from_token(token)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    description="注册新用户账户。如果未提供用户名，将自动使用邮箱前缀作为用户名。",
    responses={
        201: {
            "description": "注册成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误或邮箱已被注册",
            "content": {
                "application/json": {
                    "example": {"detail": "邮箱已被注册"}
                }
            }
        }
    },
    tags=["认证"]
)
async def register(
    req: RegisterRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    用户注册
    
    **请求参数说明：**
    - `name`: 用户名（可选），如果为空则使用邮箱前缀
    - `email`: 邮箱地址（必填），必须是有效的邮箱格式
    - `password`: 密码（必填），至少6位字符
    
    **示例请求：**
    ```json
    {
        "name": "张三",
        "email": "zhangsan@example.com",
        "password": "password123"
    }
    ```
    
    **不提供用户名的情况：**
    ```json
    {
        "email": "lisi@example.com",
        "password": "password123"
    }
    ```
    将自动使用 "lisi" 作为用户名。
    """
    return await user_service.register(req)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="用户登录",
    description="使用邮箱和密码登录，返回 JWT 访问令牌。",
    responses={
        200: {
            "description": "登录成功",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user": {
                            "id": 1,
                            "name": "张三",
                            "email": "zhangsan@example.com",
                            "created_at": "2024-01-01T00:00:00",
                            "updated_at": "2024-01-01T00:00:00"
                        }
                    }
                }
            }
        },
        401: {
            "description": "邮箱或密码错误",
            "content": {
                "application/json": {
                    "example": {"detail": "邮箱或密码错误"}
                }
            }
        }
    },
    tags=["认证"]
)
async def login(
    req: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    用户登录
    
    **请求参数说明：**
    - `email`: 注册时使用的邮箱地址
    - `password`: 用户密码
    
    **示例请求：**
    ```json
    {
        "email": "zhangsan@example.com",
        "password": "password123"
    }
    ```
    
    **返回说明：**
    - `access_token`: JWT 访问令牌，用于后续 API 请求的认证
    - `token_type`: 令牌类型，固定为 "bearer"
    - `user`: 用户信息
    
    **使用 Token：**
    在后续请求的 Header 中添加：
    ```
    Authorization: Bearer {access_token}
    ```
    """
    return await user_service.login(req)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息。需要 Bearer Token 认证。",
    responses={
        200: {
            "description": "获取成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    }
                }
            }
        },
        401: {
            "description": "未认证或 Token 无效",
            "content": {
                "application/json": {
                    "example": {"detail": "无效的认证令牌"}
                }
            }
        }
    },
    tags=["认证"]
)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    获取当前登录用户信息
    
    **认证要求：**
    需要在请求头中携带有效的 Bearer Token：
    ```
    Authorization: Bearer {your_access_token}
    ```
    
    **返回说明：**
    返回当前登录用户的完整信息，包括用户 ID、用户名、邮箱和创建/更新时间。
    """
    return current_user
