from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials, HTTPAuthorizationCredentials
from app.response import *

router = APIRouter(prefix='/api')
basic_security = HTTPBasic(auto_error=False)
bearer_security = HTTPBearer(auto_error=False)


@router.get('/logon')
async def get(
    req: Request,
    basic: Optional[HTTPBasicCredentials] = Depends(basic_security),
    bearer: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security),
):

    if basic:
        return JSONResponse({'user': basic.username, 'pass': basic.password})

    if bearer:
        return JSONResponse({'token': bearer.credentials})

    return JSONResponse({'auth': 'refreshtoken'})
