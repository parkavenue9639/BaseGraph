"""用户服务"""
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from db.mysql.model import User
from db.database import get_db
from utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from schema.request.auth import RegisterRequest, LoginRequest
from schema.response.auth import UserResponse, TokenResponse
import logging

logger = logging.getLogger(__name__)


class UserService:
    """用户服务类"""
    
    def __init__(self):
        """初始化用户服务，内部管理数据库会话"""
        self.db_instance = get_db()
    
    async def register(self, req: RegisterRequest) -> UserResponse:
        """用户注册
        
        Args:
            req: 注册请求
            
        Returns:
            用户信息
            
        Raises:
            HTTPException: 如果邮箱已存在
        """
        async with self.db_instance.get_session() as db:
            # 检查邮箱是否已存在
            stmt = select(User).where(User.email == req.email)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
            
            # 如果用户名为空，使用邮箱前缀作为用户名
            user_name = req.name
            if not user_name or user_name.strip() == "":
                user_name = req.email.split("@")[0]
                # 确保用户名不超过50个字符
                if len(user_name) > 50:
                    user_name = user_name[:50]
            
            # 创建新用户
            hashed_password = get_password_hash(req.password)
            now = datetime.utcnow()
            new_user = User(
                name=user_name,
                email=req.email,
                password=hashed_password,
                created_at=now,
                updated_at=now
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            logger.info(f"User registered: {new_user.email}")
            return UserResponse.model_validate(new_user)
    
    async def login(self, req: LoginRequest) -> TokenResponse:
        """用户登录
        
        Args:
            req: 登录请求
            
        Returns:
            Token 和用户信息
            
        Raises:
            HTTPException: 如果邮箱或密码错误
        """
        async with self.db_instance.get_session() as db:
            # 查找用户
            stmt = select(User).where(User.email == req.email)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="邮箱或密码错误"
                )
            
            # 验证密码
            if not verify_password(req.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="邮箱或密码错误"
                )
            
            # 生成 token
            access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
            
            logger.info(f"User logged in: {user.email}")
            return TokenResponse(
                access_token=access_token,
                user=UserResponse.model_validate(user)
            )
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """根据 ID 获取用户
        
        Args:
            user_id: 用户 ID
            
        Returns:
            用户信息或 None
        """
        async with self.db_instance.get_session() as db:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            return UserResponse.model_validate(user)
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """根据邮箱获取用户
        
        Args:
            email: 邮箱地址
            
        Returns:
            用户信息或 None
        """
        async with self.db_instance.get_session() as db:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            return UserResponse.model_validate(user)
    
    async def get_current_user_from_token(self, token: str) -> UserResponse:
        """从 token 获取当前用户
        
        Args:
            token: JWT token
            
        Returns:
            当前用户信息
            
        Raises:
            HTTPException: 如果 token 无效或用户不存在
        """
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证令牌",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证令牌",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = await self.get_user_by_id(int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user


# 创建全局服务实例（单例模式）
_user_service_instance: Optional[UserService] = None


def get_user_service() -> UserService:
    """获取用户服务实例（单例模式）"""
    global _user_service_instance
    if _user_service_instance is None:
        _user_service_instance = UserService()
    return _user_service_instance
