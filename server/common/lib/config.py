import os
from lib.utils import path_of


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

        cls._is_ready = True
