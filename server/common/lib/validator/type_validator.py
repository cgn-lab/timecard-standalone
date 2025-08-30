from typing import Any, Iterable, List, Literal, Set, Tuple
from pydantic import BaseModel, ValidationError
from .types import *


class IsType:

    @staticmethod
    def check(
        target: Any,
        type: Any
    ) -> Literal[True]:
        '''
        `target` の型をチェックします
        正しい場合は `True` を返します

        Args:
            targets (Any): 調査対象
            type (Any): 想定する型情報

        Returns:
            value (Literal[True]): `True` （成功時）

        Raises:
            error (ValueError): 型に対応する型モデルがない
            error (pydantic.ValidationError): 型 不整合
        '''
        # type = None の場合
        if type is None:
            return target is None

        # 型モデルを取得
        Model: BaseModel = IsType.type_map.get(type)
        if Model is None:
            raise ValueError('型モデルが登録されていません')

        # チェック
        if issubclass(Model, BaseModel):
            Model(items=target)
            return True

        else:
            if isinstance(target, Model):
                return True
            else:
                raise ValidationError('型不整合です')

    @staticmethod
    def valid(
        target: Any,
        type: Any
    ) -> bool:
        '''
        `target` の型を正誤を取得します

        Args:
            targets (Any): 調査対象
            type (Any): 想定する型情報
        '''
        # type = None の場合
        if type is None:
            return target is None

        # 型モデルを取得
        Model: BaseModel = IsType.type_map.get(type)
        if Model is None:
            # TODO: モデル不備のログを出す
            return False

        # チェック
        if issubclass(Model, BaseModel):
            try:
                Model(items=target)
                return True
            except ValidationError as e:
                return False

        else:
            return isinstance(target, Model)

    type_map = {
        int: int,
        str: str,
        bytes: bytes,
        Iterable[str]: StrIterType,
        List[str]: StrListType,
        Tuple[str, ...]: StrTupleType,
        Set[str]: StrSetType,
        Iterable[int]: IntIterType,
        List[int]: IntListType,
        Tuple[int, ...]: IntTupleType,
        Set[int]: IntSetType,
    }
