from functools import wraps
from logging import getLogger
import traceback
from typing import Any, Awaitable, Callable, Optional
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

log = getLogger('api')


def handle_exceptions(
    on_error: Optional[Callable[[Exception], Any]] = None,
):
    '''
    エンドポイント用デコレータです  
    例外が発生した場合に呼び出されます  
        - on_error を呼び出します  
        - ログにエラーを出力します  
        - セッションを閉じます  

    Args:
        on_error (Callable): エラー時に呼び出される関数
    '''
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = None
            session: AsyncSession = kwargs.get('session')
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log.error(traceback.format_exc())
                if on_error:
                    if isinstance(on_error, Awaitable):
                        result = await on_error(e)
                    else:
                        result = on_error(e)
            finally:
                if session:
                    await session.close()
                if result:
                    return result
                else:
                    return Response(status_code=500)
        return wrapper
    return decorator
