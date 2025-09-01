from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class DataBase:
    '''
    データベース接続管理クラス
    '''
    _sessionmaker: sessionmaker
    Base = Base
    engine: AsyncEngine

    @classmethod
    async def init(cls, url: str, is_dev: bool = False) -> None:
        '''
        データベース接続の初期化を行います

        Args:
            url (str): データベースのURL
            is_dev (bool): 開発中か
        '''
        cls.engine = create_async_engine(url, echo=is_dev, future=True)
        cls._sessionmaker = sessionmaker(
            bind=cls.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        await cls._apply_schemas()

    @classmethod
    async def _apply_schemas(cls) -> None:
        '''
        データベースのスキーマを同期します
        '''
        # ORMモデルを読み込み
        from lib.database import orm
        # 不足しているテーブルを作成
        async with cls.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def session(cls) -> AsyncGenerator[AsyncSession, None]:
        '''
        セッションを作成します
        '''
        async with cls._sessionmaker() as session:
            yield session

    @classmethod
    async def on_shutdown(cls) -> None:
        '''
        終了時処理です  
        シャットダウン時に呼び出します
        '''
        await cls.engine.dispose()
