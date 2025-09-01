from datetime import datetime, timedelta, timezone
from typing import Union
from argon2 import PasswordHasher
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from lib import Config, TimeZone

argon = PasswordHasher(
    time_cost=2,            # 計算時間（デフォルト 2）
    memory_cost=102400,     # メモリ使用量（KiB）
    parallelism=8,          # 並列度
    hash_len=32,            # 出力ハッシュの長さ（bytes）
    salt_len=16             # salt の長さ（bytes）
)


class AuthUtil:
    @classmethod
    def generate(cls, plain_pw: str) -> str:
        '''
        `plain_pw` をハッシュ化します

        Args:
            plain_pw (str): ハッシュ化したいパスワード（平文）
        '''
        if len(plain_pw) < 8:
            raise Exception('ハッシュ化するパスワードは8文字以上にしてください')
        return argon.hash(plain_pw + Config.PEPPER)

    @classmethod
    def verify(cls, plain_pw: str, hashed_pw: str) -> bool:
        '''
        `hashed_pw` を復元して `plain_pw` と一致するかを取得します

        Args:
            plain_pw (str): 確認したいパスワード（平文）
            hashed_pw (str): ハッシュ化したパスワード
        '''
        try:
            return argon.verify(hashed_pw, plain_pw + Config.PEPPER)
        except Exception:
            return False

    @classmethod
    def encode_jwt(cls, user_id: str) -> str:
        '''
        JWTを作成します

        Args:
            user_id (str): ユーザID
        '''

        # 有効期限
        now = datetime.now(TimeZone.UTC)
        expire = now + timedelta(minutes=Config.JWT_AVAILABLES_IN)

        # データに有効期限を付与
        payload = {
            'exp': int(expire.timestamp()),     # 有効期限
            'sub': user_id,
        }

        # JWTを発行
        jwt_content = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
        return jwt_content

    @classmethod
    async def decode_jwt(cls, jwt_content: str) -> Union[str, None]:
        '''
        JWTを復元します

        Args:
            jwt_content (str): JWT文字列
        '''
        payload: dict = jwt.decode(
            jwt_content,
            Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM])
        return payload.get('sub')

    @classmethod
    async def get_id_from_jwt(cls, jwt_content: str) -> Union[str, None]:
        '''
        JWTからユーザIDを取得します

        Args:
            jwt_content (str): JWT文字列
        '''
        # JWTを復元
        try:
            user_id = await cls.decode_jwt(jwt_content)
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        return user_id
