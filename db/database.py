from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from config.env import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class MySQLDatabase:
    """MySQL 数据库管理类
    
    负责数据库连接管理、会话管理和表初始化
    """
    
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        pool_size: int = 100,
        max_overflow: int = 30,
        pool_timeout: int = 30,
        pool_recycle: int = 3600
    ):
        """初始化数据库连接
        
        Args:
            user: 数据库用户名，默认使用环境变量
            password: 数据库密码，默认使用环境变量
            host: 数据库主机，默认使用环境变量
            port: 数据库端口，默认使用环境变量
            database: 数据库名称，默认使用环境变量
            pool_size: 连接池大小
            max_overflow: 最大溢出连接数
            pool_timeout: 连接池超时时间
            pool_recycle: 连接回收时间（秒）
        """
        self.user = user or DB_USER
        self.password = password or DB_PASSWORD
        self.host = host or DB_HOST
        self.port = port or DB_PORT
        self.database = database or DB_NAME
        
        # 配置异步数据库连接URL
        self.database_url = (
            f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
        
        # 创建异步数据库引擎
        self.engine: AsyncEngine = create_async_engine(
            self.database_url,
            pool_pre_ping=True,  # 自动检测断开的连接
            pool_recycle=pool_recycle,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )
        
        # 创建异步会话工厂
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    @asynccontextmanager
    async def get_session(self):
        """获取数据库会话上下文管理器
        
        Usage:
            async with db.get_session() as session:
                # 使用 session 进行操作
                pass
        """
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def init_tables(self) -> bool:
        """初始化数据库表
        
        扫描当前数据库以及模型，如果没有建表的自动建表
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            logger.info("Starting MySQL database initialization...")
            
            # 导入所有模型以确保它们被注册到 Base.metadata
            from db import mysql  # noqa: F401
            
            # 获取所有已定义的模型表
            metadata_tables = Base.metadata.tables
            logger.info(f"Found {len(metadata_tables)} model(s) to check: {list(metadata_tables.keys())}")
            
            # 使用已有的异步引擎检查现有表
            async with self.engine.begin() as conn:
                # 使用异步 SQL 查询检查现有表
                result = await conn.execute(
                    text("""
                        SELECT TABLE_NAME 
                        FROM INFORMATION_SCHEMA.TABLES 
                        WHERE TABLE_SCHEMA = DATABASE()
                    """)
                )
                existing_tables = {row[0] for row in result}
                logger.info(f"Existing tables in database: {existing_tables}")

                # 检查并创建每个表
                created_count = 0
                existing_count = 0
                for table_name, table in metadata_tables.items():
                    if table_name not in existing_tables:
                        logger.info(f"Creating table: {table_name}")
                        # 使用 run_sync 在异步上下文中运行同步的 create 操作
                        await conn.run_sync(lambda sync_conn, tbl=table: tbl.create(bind=sync_conn))
                        created_count += 1
                    else:
                        logger.info(f"Table already exists: {table_name}")
                        existing_count += 1
                
                logger.info(f"Table initialization summary: {created_count} created, {existing_count} already existed")
            
            logger.info("MySQL database initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"MySQL database initialization failed: {str(e)}", exc_info=True)
            return False
    
    async def close(self):
        """关闭数据库引擎"""
        await self.engine.dispose()


# 创建全局数据库实例（单例模式）
_db_instance: Optional[MySQLDatabase] = None


def get_db() -> MySQLDatabase:
    """获取全局数据库实例（单例模式）
    
    Returns:
        MySQLDatabase: 数据库实例
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = MySQLDatabase()
    return _db_instance