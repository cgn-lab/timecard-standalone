import os
from typing import Tuple
import orjson
from lib.validator import IsType


def path_of(*paths: str, as_abs: bool = True):
    '''
    パスを連結します

    Args:
        paths (str): 連結する文字列
        as_abs (bool): 絶対パスとして返す

    Returns:
        value (str): 連結後の絶対パス
    '''
    IsType.valid(paths, Tuple[str, ...])
    joined = os.path.join(*paths)
    return os.path.abspath(joined) if as_abs else joined


def read_file(path: str, as_binary: bool = False, encoding='utf-8'):
    '''
    ファイルを読み込みます

    Args:
        path (str): ファイルパス
        as_binary (bool): バイナリとして読み込む
        encoding (str): 文字コード
    '''
    # バイナリとして読み込む
    if as_binary:
        with open(path, mode='rb') as f:
            return f.read()

    if path.endswith('.json'):
        with open(path, mode='rb') as f:
            return orjson.loads(f.read())
    else:
        with open(path, mode='r', encoding=encoding) as f:
            return f.read()


__all__ = [
    'path_of',
    'read_file',
]
