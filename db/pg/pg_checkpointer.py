import logging
import sys
import asyncio
from typing import cast, Any, Optional, AsyncIterator, Sequence

# Windows事件循环策略设置 - 解决psycopg兼容性问题
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.base import (
    CheckpointTuple,
    CheckpointMetadata,
    Checkpoint,
    ChannelVersions,
    get_checkpoint_id,
    get_checkpoint_metadata,
    WRITES_IDX_MAP,
)
from langgraph.checkpoint.sqlite.utils import search_where
from langchain_core.runnables import RunnableConfig

import psycopg
from psycopg_pool import AsyncConnectionPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.pg.models import Base, Checkpoint, Write
from config.env import POSTGRES_CONN_STRING


logger = logging.getLogger(__name__)


class AsyncCompatiblePostgresSaver(AsyncSqliteSaver):
    """精简版兼容 PostgreSQL 的 checkpointer
    
    保持与 AsyncSqliteSaver 的接口和序列化兼容性，
    底层使用 PostgreSQL 存储。
    """

    def __init__(self, pool: AsyncConnectionPool, **kwargs):
        super().__init__(None, **kwargs)
        self.pool = pool

    async def setup(self):
        """使用 SQLAlchemy ORM 设置数据库表结构"""
        if not POSTGRES_CONN_STRING:
            raise ValueError("POSTGRES_CONN_STRING 未设置")
        
        # 将 postgresql:// 转换为 postgresql+psycopg:// 以便 SQLAlchemy 使用 psycopg 驱动
        sqlalchemy_url = POSTGRES_CONN_STRING.replace(
            "postgresql://", "postgresql+psycopg://", 1
        ).replace(
            "postgres://", "postgresql+psycopg://", 1
        )
        
        # 创建 SQLAlchemy 异步引擎
        engine = create_async_engine(
            sqlalchemy_url,
            echo=False,  # 设置为 True 可以查看生成的 SQL
        )
        
        try:
            # 使用 create_all 创建所有表（如果不存在）
            # 这会自动创建表、主键和索引
            async with engine.begin() as conn:
                logger.info("正在检查并创建数据库表结构...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("✅ 数据库表结构检查完成（表已存在或已创建）")
        finally:
            # 关闭引擎
            await engine.dispose()
    
    async def aget_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        """Get a checkpoint tuple from the database asynchronously.

        This method retrieves a checkpoint tuple from the SQLite database based on the
        provided config. If the config contains a "checkpoint_id" key, the checkpoint with
        the matching thread ID and checkpoint ID is retrieved. Otherwise, the latest checkpoint
        for the given thread ID is retrieved.

        Args:
            config: The config to use for retrieving the checkpoint.

        Returns:
            Optional[CheckpointTuple]: The retrieved checkpoint tuple, or None if no matching checkpoint was found.
        """
        await self.setup()
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur:
                    # find the latest checkpoint for the thread_id
                    if checkpoint_id := get_checkpoint_id(config):
                        await cur.execute(
                            "SELECT thread_id, checkpoint_id, parent_checkpoint_id, type, checkpoint, metadata FROM checkpoints WHERE thread_id = %s AND checkpoint_ns = %s AND checkpoint_id = %s",
                            (
                                str(config["configurable"]["thread_id"]),
                                checkpoint_ns,
                                checkpoint_id,
                            ),
                        )
                    else:
                        await cur.execute(
                            "SELECT thread_id, checkpoint_id, parent_checkpoint_id, type, checkpoint, metadata FROM checkpoints WHERE thread_id = %s AND checkpoint_ns = %s ORDER BY checkpoint_id DESC LIMIT 1",
                            (str(config["configurable"]["thread_id"]), checkpoint_ns),
                        )
                    # if a checkpoint is found, return it
                    if value := await cur.fetchone():
                        (
                            thread_id,
                            checkpoint_id,
                            parent_checkpoint_id,
                            type,
                            checkpoint,
                            metadata,
                        ) = value
                        if not get_checkpoint_id(config):
                            config = {
                                "configurable": {
                                    "thread_id": thread_id,
                                    "checkpoint_ns": checkpoint_ns,
                                    "checkpoint_id": checkpoint_id,
                                }
                            }
                        # find any pending writes
                        await cur.execute(
                            "SELECT task_id, channel, type, value FROM writes WHERE thread_id = %s AND checkpoint_ns = %s AND checkpoint_id = %s ORDER BY task_id, idx",
                            (
                                str(config["configurable"]["thread_id"]),
                                checkpoint_ns,
                                str(config["configurable"]["checkpoint_id"]),
                            ),
                        )
                        # deserialize the checkpoint and metadata
                        return CheckpointTuple(
                            config,
                            self.serde.loads_typed((type, checkpoint)),
                            cast(
                                CheckpointMetadata,
                                self.jsonplus_serde.loads(metadata)
                                if metadata is not None
                                else {},
                            ),
                            (
                                {
                                    "configurable": {
                                        "thread_id": thread_id,
                                        "checkpoint_ns": checkpoint_ns,
                                        "checkpoint_id": parent_checkpoint_id,
                                    }
                                }
                                if parent_checkpoint_id
                                else None
                            ),
                            [
                                (task_id, channel, self.serde.loads_typed((type, value)))
                                async for task_id, channel, type, value in cur
                            ],
                        )

    async def alist(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[CheckpointTuple]:
        """List checkpoints from the database asynchronously.

        This method retrieves a list of checkpoint tuples from the SQLite database based
        on the provided config. The checkpoints are ordered by checkpoint ID in descending order (newest first).

        Args:
            config: Base configuration for filtering checkpoints.
            filter: Additional filtering criteria for metadata.
            before: If provided, only checkpoints before the specified checkpoint ID are returned. Defaults to None.
            limit: Maximum number of checkpoints to return.

        Yields:
            AsyncIterator[CheckpointTuple]: An asynchronous iterator of matching checkpoint tuples.
        """
        await self.setup()
        where, params = search_where(config, filter, before)
        query = f"""SELECT thread_id, checkpoint_ns, checkpoint_id, parent_checkpoint_id, type, checkpoint, metadata
        FROM checkpoints
        {where}
        ORDER BY checkpoint_id DESC"""
        if limit:
            query += f" LIMIT {limit}"
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur, conn.cursor() as wcur:
                    await cur.execute(query, params)
                    async for (
                        thread_id,
                        checkpoint_ns,
                        checkpoint_id,
                        parent_checkpoint_id,
                        type,
                        checkpoint,
                        metadata,
                    ) in cur:
                        await wcur.execute(
                            "SELECT task_id, channel, type, value FROM writes WHERE thread_id = %s AND checkpoint_ns = %s AND checkpoint_id = %s ORDER BY task_id, idx",
                            (thread_id, checkpoint_ns, checkpoint_id),
                        )
                        yield CheckpointTuple(
                            {
                                "configurable": {
                                    "thread_id": thread_id,
                                    "checkpoint_ns": checkpoint_ns,
                                    "checkpoint_id": checkpoint_id,
                                }
                            },
                            self.serde.loads_typed((type, checkpoint)),
                            cast(
                                CheckpointMetadata,
                                self.jsonplus_serde.loads(metadata)
                                if metadata is not None
                                else {},
                            ),
                            (
                                {
                                    "configurable": {
                                        "thread_id": thread_id,
                                        "checkpoint_ns": checkpoint_ns,
                                        "checkpoint_id": parent_checkpoint_id,
                                    }
                                }
                                if parent_checkpoint_id
                                else None
                            ),
                            [
                                (task_id, channel, self.serde.loads_typed((type, value)))
                                async for task_id, channel, type, value in wcur
                            ],
                        )

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Save a checkpoint to the database asynchronously.

        This method saves a checkpoint to the SQLite database. The checkpoint is associated
        with the provided config and its parent config (if any).

        Args:
            config: The config to associate with the checkpoint.
            checkpoint: The checkpoint to save.
            metadata: Additional metadata to save with the checkpoint.
            new_versions: New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.
        """
        await self.setup()
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"]["checkpoint_ns"]
        type_, serialized_checkpoint = self.serde.dumps_typed(checkpoint)
        serialized_metadata = self.jsonplus_serde.dumps(
            get_checkpoint_metadata(config, metadata)
        )
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur:
                    await cur.execute(
                        """INSERT INTO checkpoints (thread_id, checkpoint_ns, checkpoint_id, parent_checkpoint_id, type, checkpoint, metadata) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                           ON CONFLICT (thread_id, checkpoint_ns, checkpoint_id)
                           DO UPDATE SET 
                               parent_checkpoint_id = EXCLUDED.parent_checkpoint_id,
                               type = EXCLUDED.type,
                               checkpoint = EXCLUDED.checkpoint,
                               metadata = EXCLUDED.metadata""",
                        (
                            str(config["configurable"]["thread_id"]),
                            checkpoint_ns,
                            checkpoint["id"],
                            config["configurable"].get("checkpoint_id"),
                            type_,
                            serialized_checkpoint,
                            serialized_metadata,
                        ),
                    )
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint["id"],
            }
        }

    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store intermediate writes linked to a checkpoint asynchronously.

        This method saves intermediate writes associated with a checkpoint to the database.

        Args:
            config: Configuration of the related checkpoint.
            writes: List of writes to store, each as (channel, value) pair.
            task_id: Identifier for the task creating the writes.
            task_path: Path of the task creating the writes.
        """
        query = (
            """INSERT INTO writes (thread_id, checkpoint_ns, checkpoint_id, task_id, idx, channel, type, value) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
               DO UPDATE SET 
                   channel = EXCLUDED.channel,
                   type = EXCLUDED.type,
                   value = EXCLUDED.value"""
            if all(w[0] in WRITES_IDX_MAP for w in writes)
            else """INSERT INTO writes (thread_id, checkpoint_ns, checkpoint_id, task_id, idx, channel, type, value) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
                    DO NOTHING"""
        )
        await self.setup()
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur:
                    await cur.executemany(
                        query,
                        [
                            (
                                str(config["configurable"]["thread_id"]),
                                str(config["configurable"]["checkpoint_ns"]),
                                str(config["configurable"]["checkpoint_id"]),
                                task_id,
                                WRITES_IDX_MAP.get(channel, idx),
                                channel,
                                *self.serde.dumps_typed(value),
                            )
                            for idx, (channel, value) in enumerate(writes)
                        ],
                    )

    async def adelete_thread(self, thread_id: str) -> None:
        """Delete all checkpoints and writes associated with a thread ID.

        Args:
            thread_id: The thread ID to delete.

        Returns:
            None
        """
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur:
                    await cur.execute(
                        "DELETE FROM checkpoints WHERE thread_id = %s",
                        (str(thread_id),),
                    )
                    await cur.execute(
                        "DELETE FROM writes WHERE thread_id = %s",
                        (str(thread_id),),
                    )

    async def aclose(self) -> None:
        """Close the underlying connection pool."""
        try:
            await self.pool.close()
        except Exception:
            pass
