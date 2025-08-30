from typing import List, Tuple, Set, Iterable
from pydantic import BaseModel, field_validator


class StrIterType(BaseModel):
    items: Iterable[str]

    @field_validator('items')
    @classmethod
    def reject_str(cls, v):
        if isinstance(v, (str, bytes)):
            raise TypeError('items must be a non-string iterable of str')
        return v


class StrListType(BaseModel):
    items: List[str]


class StrTupleType(BaseModel):
    items: Tuple[str, ...]


class StrSetType(BaseModel):
    items: Set[str]


class IntIterType(BaseModel):
    items: Iterable[int]

    @field_validator('items')
    @classmethod
    def reject_str(cls, v):
        if isinstance(v, (str, bytes)):
            raise TypeError('items must be a non-string iterable of int')
        return v


class IntListType(BaseModel):
    items: List[int]


class IntTupleType(BaseModel):
    items: Tuple[int, ...]


class IntSetType(BaseModel):
    items: Set[int]


__all__ = [
    'StrIterType',
    'StrListType',
    'StrTupleType',
    'StrSetType',
    'IntIterType',
    'IntListType',
    'IntTupleType',
    'IntSetType',
]
