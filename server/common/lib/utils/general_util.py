import os
from typing import Tuple
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


__all__ = [
    'path_of',
]
