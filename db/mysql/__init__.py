"""
MySQL 数据库模型模块
统一导入所有模型，确保它们被注册到 Base.metadata
"""
from db.mysql.model import User  # noqa: F401

__all__ = ["User"]
