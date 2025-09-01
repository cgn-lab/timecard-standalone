from datetime import datetime, timedelta, timezone
from logging import getLogger
import secrets
from typing import Optional
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.response import *
from lib import TimeZone
from lib.database import DB
from lib.database.orm import AuthCredentials
from lib.utils import AuthUtil
from lib.utils.decorators import handle_exceptions

log = getLogger('api')
router = APIRouter(prefix='/api')
basic_security = HTTPBasic(auto_error=False)
bearer_security = HTTPBearer(auto_error=False)


@router.get('/logon')
@handle_exceptions()
async def get(
    req: Request,
    basic: Optional[HTTPBasicCredentials] = Depends(basic_security),
    bearer: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security),
    session: AsyncSession = Depends(DB.session),
):
    log.debug('/api/logon: アクセスログ')

    # データ取得
    headers = req.headers
    header_accept = headers.get('Accept')
    if header_accept != 'application/json':
        log.debug(f'ヘッダ不一致: {header_accept}')
        return Response(status_code=400)

    now = datetime.now(TimeZone.JST)

    if basic:

        # usernameで検索
        cred = await AuthCredentials.by_username(username=basic.username, session=session)
        if not cred:
            log.debug('一致するユーザが見つかりません')
            return Response(status_code=401)

        # END: パスワード不一致
        if not AuthUtil.verify(plain_pw=basic.password, hashed_pw=cred.password):
            log.debug('ユーザのパスワードが一致しません')
            return Response(status_code=401)

        log.debug(f'有効なユーザ: {cred.id}')

        # 重複しないトークンを生成
        is_duplicated = True
        while is_duplicated:
            token = secrets.token_hex(32)
            is_duplicated = bool(await AuthCredentials.by_token(token=token, session=session))
        log.debug('新規のリフレッシュトークンが発行されました')

        # レコードを更新
        cred.token = token
        cred.token_due = now + timedelta(days=7)
        await session.commit()

        # レスポンスを返す
        response = JSONResponse({
            'JWT': AuthUtil.encode_jwt(str(cred.id)),
        })

        cookie_expire = (now + timedelta(days=7)).astimezone(timezone.utc)
        response.set_cookie(
            key='access_token',         # Cookie キー
            value=token,                # Cookie 値
            httponly=True,              # HTTP Only
            max_age=7*24*60*60,         # 7日
            expires=cookie_expire.strftime('%a, %d-%b-%Y %H:%M:%S GMT'),
            secure=False,               # HTTPS
            samesite='lax',             # strict, none, lax
            path='/',                   # Cookie を有効にするパス
        )
        return response

    if bearer:

        # JWTを復元
        log.debug(f'JWTトークン: あり')
        user_id = await AuthUtil.get_id_from_jwt(bearer.credentials)
        if not user_id:
            log.debug(f'JWT: ユーザ情報なし')
            return Response(status_code=401)
        # END: ユーザを検索
        cred = await AuthCredentials.by_id(user_id, session)
        if cred is None:
            log.debug(f'JWT: ユーザIDと一致するユーザなし ({user_id})')
            return Response(status_code=401)

        # JWT期限を更新
        response = JSONResponse({
            'JWT': AuthUtil.encode_jwt(str(cred.id)),
        })

        return response

    # リフレッシュトークンから再発行

    # リフレッシュトークンを取得
    access_token = req.cookies.get('access_token')
    if not access_token:
        log.debug(f'リフレッシュトークン: なし')
        return Response(status_code=401)

    # トークンからユーザを取得
    cred = await AuthCredentials.by_token(token=access_token, session=session)
    if cred is None:
        log.debug(f'リフレッシュトークンと一致するユーザ: なし')
        return Response(status_code=401)

    # トークンの有効期限を取得
    if cred.token_due < now:
        return Response(status_code=401)

    # JWT期限を更新
    response = JSONResponse({
        'JWT': AuthUtil.encode_jwt(str(cred.id)),
    })

    return response
