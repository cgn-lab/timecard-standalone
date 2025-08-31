import os
from lib.utils import path_of, read_file


class Config:
    _is_ready: bool = False

    ROOT_DIR: str

    @classmethod
    def init(cls):
        ''' 初期化処理 '''

        if cls._is_ready:
            return

        this_file = os.path.abspath(__file__)
        cls.ROOT_DIR = path_of(this_file, '..', '..', '..')
        cls.PUBLIC_DIR = path_of(cls.ROOT_DIR, '..', 'public')

        # データベース接続情報
        config = read_file(path_of(cls.ROOT_DIR, 'config', 'settings.yaml'))
        db_config = config['database']
        db_host = db_config['host']
        db_port = db_config['port']
        db_user = db_config['user']
        db_pass = db_config['pass']
        db_name = db_config['name']
        cls.DB_URL = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

        cls._is_ready = True
