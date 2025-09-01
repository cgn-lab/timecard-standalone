from fastapi import APIRouter, Depends, Request
from logging import getLogger
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.response import *
from app.schemas import PostRegisterRequest
from lib.database import DB
from lib.database.orm import AuthCredentials
from lib.utils import AuthUtil
from lib.utils.decorators import handle_exceptions

log = getLogger('api')
router = APIRouter(prefix='/api')
bearer_security = HTTPBearer(auto_error=False)


@router.post('/register')
@handle_exceptions()
async def post(
    request: Request,
    body: PostRegisterRequest,
    bearer: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security),
    session: AsyncSession = Depends(DB.session),
):
    # ヘッダ取得
    headers = request.headers
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        log.debug(f'ヘッダ不一致 Content-Type: {content_type}')
        return Response(status_code=400)
    accept = headers.get('Accept')
    if accept != 'application/json':
        log.debug(f'ヘッダ不一致 Accept: {accept}')
        return Response(status_code=400)

    # トークン検証
    if bearer:
        # JWTを復元
        log.debug(f'JWTトークン: あり')
        user_id = AuthUtil.get_id_from_jwt(bearer.credentials)
        if not user_id:
            log.debug(f'JWT: ユーザ情報なし')
            return Response(status_code=401)
        # END: ユーザを検索
        cred = await AuthCredentials.by_id(user_id, session)
        if cred is None:
            log.debug(f'JWT: ユーザIDと一致するユーザなし ({user_id})')
            return Response(status_code=401)
    else:
        # 初期登録のみ JWTなしで登録可能
        # END: 1件もレコードが存在しない場合
        log.debug(f'JWTトークン: なし')
        query = select(func.count()).select_from(AuthCredentials)
        result = await session.execute(query)
        count = result.scalar()
        if 0 < count:
            log.debug(f'初期ユーザ作成... 拒否')
            return Response(status_code=401)
        log.info(f'初期ユーザ作成')

    # END: 4文字未満の名前・8文字未満のパスワード
    if len(body.username) < 4:
        return Response(status_code=400)
    if len(body.password) < 8:
        return Response(status_code=400)

    username = body.username
    password = AuthUtil.generate(body.password)

    # レコードを作成
    new_cred = AuthCredentials(
        username=username,
        password=password,
        created_by=user_id if bearer else None,
        updated_by=user_id if bearer else None,
    )
    session.add(new_cred)
    await session.commit()
    log.info(f'新規ユーザ作成: {new_cred.id}')

    # レスポンスを返す
    return Response(status_code=200)
