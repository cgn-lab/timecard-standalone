import os
from logging.config import dictConfig


class Config:
    _is_ready: bool = False

    ROOT_DIR: str
    PUBLIC_DIR: str

    DB_URL: str

    PEPPER: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_AVAILABLES_IN: int

    @classmethod
    def init(cls):
        ''' 初期化処理 '''
        from lib.utils import path_of, read_file

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

        auth_config = config['auth']
        cls.PEPPER = auth_config['pepper']
        jwt_config = auth_config['jwt']
        cls.JWT_SECRET = jwt_config['secret']                   # JWT暗号化用キー
        cls.JWT_ALGORITHM = jwt_config['algorithm']             # JWT暗号化方式
        cls.JWT_AVAILABLES_IN = jwt_config['available_min']     # JWT有効期限

        # ロガー設定
        LOG_DIR = path_of(cls.ROOT_DIR, 'logs')
        os.makedirs(LOG_DIR, exist_ok=True)
        log_config = read_file(path_of(cls.ROOT_DIR, 'config', 'logger.yaml'))
        dictConfig(log_config)

        cls._is_ready = True
