import os
import sys
from fastapi import FastAPI


# ディレクトリ移動
EXEC_DIR = os.path.abspath(
    os.path.join(os.path.abspath(__file__), '..', '..'))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, '..'))
os.chdir(EXEC_DIR)
# 共通処理を環境変数に追加
sys.path.append(os.path.join(ROOT_DIR, 'common'))


async def lifespan(app: FastAPI):
    ''' FastAPI 前処理・後処理 '''
    # 前処理
    from app.routers import load_routers
    from lib.config import Config
    from lib.database import DB

    # 設定を初期化
    Config.init()

    # データベース接続設定の初期化
    await DB.init(Config.DB_URL)

    # ルータを設定
    for router in load_routers():
        app.include_router(router)

    yield

    # 後処理
    pass


app = FastAPI(lifespan=lifespan)
