"""
PostgreSQL 数据库模型定义
使用 SQLAlchemy ORM
"""
from sqlalchemy import (
    Column, String, LargeBinary, BigInteger, Index, 
    PrimaryKeyConstraint, Text
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


class Checkpoint(Base):
    """Checkpoints 表模型"""
    __tablename__ = "checkpoints"
    
    thread_id = Column(Text, nullable=False)
    checkpoint_ns = Column(Text, nullable=False, default="", server_default="")
    checkpoint_id = Column(Text, nullable=False)
    parent_checkpoint_id = Column(Text, nullable=True)
    type = Column(Text, nullable=True)
    checkpoint = Column(LargeBinary, nullable=True)  # BYTEA in PostgreSQL
    # 使用 name 参数将 Python 属性名映射到数据库列名 'metadata'
    checkpoint_metadata = Column("metadata", LargeBinary, nullable=True)  # BYTEA in PostgreSQL
    
    __table_args__ = (
        PrimaryKeyConstraint("thread_id", "checkpoint_ns", "checkpoint_id"),
        Index("idx_checkpoints_thread_id", "thread_id"),
        Index("idx_checkpoints_thread_ns", "thread_id", "checkpoint_ns"),
    )


class Write(Base):
    """Writes 表模型"""
    __tablename__ = "writes"
    
    thread_id = Column(Text, nullable=False)
    checkpoint_ns = Column(Text, nullable=False, default="", server_default="")
    checkpoint_id = Column(Text, nullable=False)
    task_id = Column(Text, nullable=False)
    idx = Column(BigInteger, nullable=False)
    channel = Column(Text, nullable=False)
    type = Column(Text, nullable=True)
    value = Column(LargeBinary, nullable=True)  # BYTEA in PostgreSQL
    
    __table_args__ = (
        PrimaryKeyConstraint("thread_id", "checkpoint_ns", "checkpoint_id", "task_id", "idx"),
        Index("idx_writes_thread_id", "thread_id"),
        Index("idx_writes_thread_ns", "thread_id", "checkpoint_ns"),
        Index("idx_writes_checkpoint_id", "checkpoint_id"),
    )

