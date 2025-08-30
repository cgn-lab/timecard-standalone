import os
import sys
from fastapi import FastAPI


# ディレクトリ移動
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.abspath(__file__), '..', '..', '..'))
os.chdir(ROOT_DIR)
# 共通処理を環境変数に追加
sys.path.append(os.path.join(ROOT_DIR, 'common'))


async def lifespan(app: FastAPI):
    ''' FastAPI 前処理・後処理 '''
    # 前処理
    from lib.config import Config
    Config.init()

    yield

    # 後処理
    pass


app = FastAPI(lifespan=lifespan)
